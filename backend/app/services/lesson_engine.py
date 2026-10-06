"""Lesson attempts: start, resume, answer, quit, and the finalize step that awards a lesson.

Every public function commits once at the end, so a request either applies all of its
changes or none of them.
"""

import random
from datetime import date, datetime
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import (
    AttemptAnswer,
    DailyActivity,
    Exercise,
    Lesson,
    LessonAttempt,
    Skill,
    User,
    UserSkillProgress,
)
from app.models.content import PERFECT_LESSON_BONUS_XP
from app.schemas.attempt_result import AchievementUnlock, AttemptResult, DailyGoalResult
from app.schemas.exercises import EXERCISE_ADAPTER, ExercisePublic
from app.schemas.lesson import (
    AnsweredExercise,
    AnswerResponse,
    AttemptResponse,
    LessonInfo,
    QuitResponse,
)
from app.services import achievements, clock, grading, hearts, path, streak

IN_PROGRESS = "in_progress"
COMPLETED = "completed"
FAILED = "failed"
ABANDONED = "abandoned"


def start_lesson(db: Session, user: User, skill_id: int) -> AttemptResponse:
    """Open an attempt on the skill's next lesson, or a random one if the skill is done."""
    state = path.skill_states(db, user).get(skill_id)
    if state is None:
        raise AppError("NOT_FOUND", "That skill does not exist.", 404)
    if state == path.LOCKED:
        raise AppError("SKILL_LOCKED", "Complete all levels above to unlock this!", 403)
    now = clock.user_now(db, user)
    hearts.apply_regen(user.stats, now)
    if user.stats.hearts == 0:
        raise AppError("NO_HEARTS", "You have no hearts left.", 409)
    skill = db.get_one(Skill, skill_id)
    lesson, mode = _next_lesson(db, user, skill, is_skill_completed=state == path.COMPLETED)
    _abandon_open_attempts(db, user, now)
    attempt = LessonAttempt(
        user=user,
        lesson=lesson,
        mode=mode,
        status=IN_PROGRESS,
        mistakes=0,
        xp_earned=0,
        started_at=now,
    )
    db.add(attempt)
    db.commit()
    return _attempt_response(attempt, user.stats.hearts)


def get_attempt(db: Session, user: User, attempt_id: int) -> AttemptResponse:
    """The attempt as it stands, so a refreshed page can rebuild the lesson player."""
    attempt = _owned_attempt(db, user, attempt_id)
    if hearts.apply_regen(user.stats, clock.user_now(db, user)):
        db.commit()
    return _attempt_response(attempt, user.stats.hearts)


def submit_answer(
    db: Session, user: User, attempt_id: int, exercise_id: int, raw_answer: dict[str, Any]
) -> AnswerResponse:
    attempt = _owned_attempt(db, user, attempt_id)
    exercise = _exercise_in_attempt(attempt, exercise_id)
    if attempt.status == COMPLETED:
        # Idempotent finalize: a retried or double-clicked completing answer gets the stored
        # result back and can never award XP a second time.
        return _completed_response(attempt, user.stats.hearts)
    if attempt.status != IN_PROGRESS:
        raise AppError("ATTEMPT_CLOSED", "This lesson is no longer in progress.", 409)
    # Read before this answer is recorded, so the set holds only earlier correct answers.
    already_correct_ids = _correct_exercise_ids(attempt)
    if exercise.id in already_correct_ids:
        raise AppError("EXERCISE_ALREADY_CORRECT", "That exercise is already done.", 409)
    outcome = grading.grade(exercise, raw_answer)
    now = clock.user_now(db, user)
    hearts.apply_regen(user.stats, now)
    _record_answer(db, attempt, exercise, raw_answer, is_correct=outcome.is_correct, now=now)
    result = None
    if not outcome.is_correct and outcome.costs_heart:
        _charge_mistake(attempt, user, now)
    elif outcome.is_correct and already_correct_ids | {exercise.id} == _exercise_ids(attempt):
        if not _claim_completion(db, attempt):
            # A simultaneous request finished this attempt first. Drop this request's writes
            # and answer exactly as a retry would; the rollback reloads the stored result.
            db.rollback()
            return _completed_response(attempt, user.stats.hearts)
        result = _finalize(db, user, attempt, now)
    db.commit()
    return AnswerResponse(
        correct=outcome.is_correct,
        correct_solution=outcome.correct_solution,
        feedback_note=outcome.feedback_note,
        hearts=user.stats.hearts,
        status=attempt.status,
        result=result,
    )


def quit_attempt(db: Session, user: User, attempt_id: int) -> QuitResponse:
    """Close an in-progress attempt; hearts already lost stay lost, as in Duolingo."""
    attempt = _owned_attempt(db, user, attempt_id)
    if attempt.status == IN_PROGRESS:
        attempt.status = ABANDONED
        attempt.finished_at = clock.user_now(db, user)
        db.commit()
    return QuitResponse(status=attempt.status)


def reopen_failed_attempt(db: Session, user: User) -> None:
    """After a refill, let the learner continue the lesson they just ran out of hearts in.

    Only the most recent attempt is reopened; an older failure was already left behind.
    """
    latest = db.scalars(
        select(LessonAttempt)
        .where(LessonAttempt.user_id == user.id)
        .order_by(LessonAttempt.id.desc())
        .limit(1)
    ).first()
    if latest is not None and latest.status == FAILED:
        latest.status = IN_PROGRESS
        latest.finished_at = None


def accuracy_percent(exercise_count: int, mistakes: int) -> int:
    """Whole percent of checks that were right: every exercise once, plus each mistake."""
    return round(100 * exercise_count / (exercise_count + mistakes))


def _next_lesson(
    db: Session, user: User, skill: Skill, *, is_skill_completed: bool
) -> tuple[Lesson, str]:
    if is_skill_completed:
        # A finished skill is replayed as practice: XP, but no change to its progress.
        return random.choice(skill.lessons), "practice"
    progress = db.get(UserSkillProgress, (user.id, skill.id))
    lessons_completed = progress.lessons_completed if progress else 0
    return skill.lessons[lessons_completed], "learn"


def _abandon_open_attempts(db: Session, user: User, now: datetime) -> None:
    # One in-progress attempt per learner, so a stale tab can never finalize twice.
    open_attempts = db.scalars(
        select(LessonAttempt).where(
            LessonAttempt.user_id == user.id, LessonAttempt.status == IN_PROGRESS
        )
    )
    for open_attempt in open_attempts:
        open_attempt.status = ABANDONED
        open_attempt.finished_at = now


def _owned_attempt(db: Session, user: User, attempt_id: int) -> LessonAttempt:
    attempt = db.get(LessonAttempt, attempt_id)
    # Another learner's attempt is reported as missing rather than forbidden.
    if attempt is None or attempt.user_id != user.id:
        raise AppError("NOT_FOUND", "That lesson attempt does not exist.", 404)
    return attempt


def _exercise_in_attempt(attempt: LessonAttempt, exercise_id: int) -> Exercise:
    for exercise in attempt.lesson.exercises:
        if exercise.id == exercise_id:
            return exercise
    raise AppError("EXERCISE_NOT_IN_ATTEMPT", "That exercise is not part of this lesson.", 400)


def _exercise_ids(attempt: LessonAttempt) -> set[int]:
    return {exercise.id for exercise in attempt.lesson.exercises}


def _correct_exercise_ids(attempt: LessonAttempt) -> set[int]:
    return {answer.exercise_id for answer in attempt.answers if answer.is_correct}


def _record_answer(
    db: Session,
    attempt: LessonAttempt,
    exercise: Exercise,
    raw_answer: dict[str, Any],
    *,
    is_correct: bool,
    now: datetime,
) -> None:
    db.add(
        AttemptAnswer(
            attempt=attempt,
            exercise=exercise,
            submitted=raw_answer,
            is_correct=is_correct,
            answered_at=now,
        )
    )


def _charge_mistake(attempt: LessonAttempt, user: User, now: datetime) -> None:
    attempt.mistakes += 1
    hearts.lose_heart(user.stats, now)
    if user.stats.hearts == 0:
        # Failed, not abandoned: a gem refill can reopen it (see reopen_failed_attempt).
        attempt.status = FAILED
        attempt.finished_at = now


def _claim_completion(db: Session, attempt: LessonAttempt) -> bool:
    """Move the attempt from in progress to completed in one conditional UPDATE.

    Two simultaneous completing answers can both read the attempt as in progress, but the
    WHERE clause is re-checked when each UPDATE runs, so only one of them changes a row.
    Returns False for the one that lost.
    """
    claimed = db.execute(
        update(LessonAttempt)
        .where(LessonAttempt.id == attempt.id, LessonAttempt.status == IN_PROGRESS)
        .values(status=COMPLETED)
        .execution_options(synchronize_session=False)
    )
    return claimed.rowcount == 1


def _finalize(db: Session, user: User, attempt: LessonAttempt, now: datetime) -> AttemptResult:
    """Award a completed lesson. Runs inside the answer request's transaction."""
    today = now.date()
    xp_earned = attempt.lesson.xp_reward + (PERFECT_LESSON_BONUS_XP if attempt.mistakes == 0 else 0)
    attempt.status = COMPLETED
    attempt.finished_at = now
    attempt.xp_earned = xp_earned
    user.stats.total_xp += xp_earned
    xp_before, xp_after = _add_daily_activity(db, user, today, xp_earned)
    streak_result = streak.record_lesson_day(user.stats, today)
    is_skill_completed = False
    if attempt.mode == "learn":
        # Practice replays earn XP but never move a skill's progress.
        is_skill_completed = _advance_skill_progress(db, user, attempt, now)
    # Last, so the counts above (streak, skills, lessons) are what the thresholds see.
    unlocked = achievements.unlock_new(db, user, now)
    exercise_count = len(attempt.lesson.exercises)
    result = AttemptResult(
        xp_earned=xp_earned,
        accuracy=accuracy_percent(exercise_count, attempt.mistakes),
        mistakes=attempt.mistakes,
        duration_s=int((now - attempt.started_at).total_seconds()),
        streak=streak_result,
        daily_goal=DailyGoalResult(
            today_xp=xp_after,
            goal_xp=user.daily_goal_xp,
            just_met=xp_before < user.daily_goal_xp <= xp_after,
        ),
        skill_completed=is_skill_completed,
        achievements_unlocked=[
            AchievementUnlock(code=item.code, title=item.title, icon=item.icon) for item in unlocked
        ],
    )
    attempt.result = result.model_dump(mode="json")
    return result


def _add_daily_activity(db: Session, user: User, today: date, xp: int) -> tuple[int, int]:
    """Add the lesson to today's row, creating it if needed; returns today's XP before and after."""
    activity = db.get(DailyActivity, (user.id, today))
    if activity is None:
        activity = DailyActivity(user=user, activity_date=today, xp_earned=0, lessons_completed=0)
        db.add(activity)
    xp_before = activity.xp_earned
    activity.xp_earned += xp
    activity.lessons_completed += 1
    return xp_before, activity.xp_earned


def _advance_skill_progress(db: Session, user: User, attempt: LessonAttempt, now: datetime) -> bool:
    """Count the lesson toward its skill; True if this lesson finished the skill."""
    skill = attempt.lesson.skill
    progress = db.get(UserSkillProgress, (user.id, skill.id))
    if progress is None:
        progress = UserSkillProgress(user=user, skill=skill, lessons_completed=0, updated_at=now)
        db.add(progress)
    progress.lessons_completed += 1
    progress.updated_at = now
    if progress.lessons_completed == len(skill.lessons):
        progress.completed_at = now
        return True
    return False


def _public_exercise(exercise: Exercise) -> ExercisePublic:
    # Parse through the full definition so the payload gets its proper model, then drop the
    # solution: the client must never receive it.
    definition = EXERCISE_ADAPTER.validate_python(
        {
            "type": exercise.type,
            "prompt": exercise.prompt,
            "payload": exercise.payload,
            "solution": exercise.solution,
        }
    )
    return ExercisePublic(
        id=exercise.id, type=exercise.type, prompt=exercise.prompt, payload=definition.payload
    )


def _attempt_response(attempt: LessonAttempt, current_hearts: int) -> AttemptResponse:
    lesson = attempt.lesson
    return AttemptResponse(
        attempt_id=attempt.id,
        mode=attempt.mode,
        status=attempt.status,
        lesson=LessonInfo(id=lesson.id, position=lesson.position, skill_title=lesson.skill.title),
        exercises=[_public_exercise(exercise) for exercise in lesson.exercises],
        hearts=current_hearts,
        answered=[
            AnsweredExercise(exercise_id=answer.exercise_id, is_correct=answer.is_correct)
            for answer in attempt.answers
        ],
        result=AttemptResult.model_validate(attempt.result) if attempt.result else None,
    )


def _completed_response(attempt: LessonAttempt, current_hearts: int) -> AnswerResponse:
    return AnswerResponse(
        correct=True,
        correct_solution=None,
        feedback_note=None,
        hearts=current_hearts,
        status=COMPLETED,
        result=AttemptResult.model_validate(attempt.result),
    )
