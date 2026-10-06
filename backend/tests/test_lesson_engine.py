from datetime import timedelta

import pytest
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import (
    AttemptAnswer,
    DailyActivity,
    Exercise,
    LessonAttempt,
    Skill,
    Unit,
    User,
    UserSkillProgress,
)
from app.schemas.lesson import AnswerResponse, AttemptResponse
from app.seed.attempt_history import CORRECT_SUBMISSIONS, WRONG_SUBMISSIONS
from app.seed.run import DEMO_USER_ID
from app.services import clock, dev_tools, leaderboard, lesson_engine, path, profile
from app.services.hearts import REFILL_COST_GEMS


def skill_at(db: Session, unit_position: int, skill_position: int) -> Skill:
    return db.scalars(
        select(Skill)
        .join(Unit)
        .where(Unit.position == unit_position, Skill.position == skill_position)
    ).one()


def answer(
    db: Session, user: User, attempt: AttemptResponse, exercise_id: int, *, is_correct: bool
) -> AnswerResponse:
    exercise = db.get_one(Exercise, exercise_id)
    builders = CORRECT_SUBMISSIONS if is_correct else WRONG_SUBMISSIONS
    return lesson_engine.submit_answer(
        db, user, attempt.attempt_id, exercise_id, builders[exercise.type](exercise)
    )


def play_correctly(db: Session, user: User, attempt: AttemptResponse) -> AnswerResponse:
    """Answer every exercise correctly in order; returns the completing response."""
    responses = [
        answer(db, user, attempt, exercise.id, is_correct=True) for exercise in attempt.exercises
    ]
    return responses[-1]


def test_full_lesson_with_one_mistake(seeded_db: Session, demo_user: User) -> None:
    skill_four = skill_at(seeded_db, 1, 4)
    attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_four.id)
    assert attempt.mode == "learn" and attempt.lesson.position == 2 and attempt.hearts == 4

    first_exercise = attempt.exercises[0]
    wrong = answer(seeded_db, demo_user, attempt, first_exercise.id, is_correct=False)
    assert not wrong.correct and wrong.hearts == 3 and wrong.correct_solution

    completing = play_correctly(seeded_db, demo_user, attempt)
    result = completing.result
    assert completing.status == "completed" and result is not None
    assert (result.xp_earned, result.mistakes, result.accuracy) == (10, 1, 89)
    assert (result.streak.count, result.streak.extended) == (7, True)
    assert [unlock.code for unlock in result.achievements_unlocked] == ["wildfire"]
    assert not result.skill_completed

    stats = demo_user.stats
    assert (stats.total_xp, stats.hearts, stats.current_streak) == (125, 3, 7)
    progress = seeded_db.get_one(UserSkillProgress, (demo_user.id, skill_four.id))
    assert progress.lessons_completed == 2


def test_completed_attempt_returns_the_identical_stored_result(
    seeded_db: Session, demo_user: User
) -> None:
    attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_at(seeded_db, 1, 4).id)
    completing = play_correctly(seeded_db, demo_user, attempt)
    total_xp_after_first_award = demo_user.stats.total_xp

    last_exercise_id = attempt.exercises[-1].id
    replay = answer(seeded_db, demo_user, attempt, last_exercise_id, is_correct=True)
    reloaded = lesson_engine.get_attempt(seeded_db, demo_user, attempt.attempt_id)

    assert replay.result == completing.result
    assert reloaded.result == completing.result
    assert demo_user.stats.total_xp == total_xp_after_first_award


def test_perfect_lesson_earns_the_bonus(seeded_db: Session, demo_user: User) -> None:
    attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_at(seeded_db, 1, 4).id)
    result = play_correctly(seeded_db, demo_user, attempt).result
    assert result is not None and (result.xp_earned, result.accuracy) == (15, 100)


def test_locked_skill_cannot_be_started(seeded_db: Session, demo_user: User) -> None:
    with pytest.raises(AppError) as raised:
        lesson_engine.start_lesson(seeded_db, demo_user, skill_at(seeded_db, 2, 1).id)
    assert (raised.value.code, raised.value.status) == ("SKILL_LOCKED", 403)


def test_no_hearts_blocks_a_start(seeded_db: Session, demo_user: User) -> None:
    demo_user.stats.hearts = 0
    demo_user.stats.hearts_updated_at = clock.user_now(seeded_db, demo_user)
    with pytest.raises(AppError) as raised:
        lesson_engine.start_lesson(seeded_db, demo_user, skill_at(seeded_db, 1, 4).id)
    assert raised.value.code == "NO_HEARTS"


def test_running_out_of_hearts_fails_and_a_refill_reopens(
    seeded_db: Session, demo_user: User
) -> None:
    attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_at(seeded_db, 1, 4).id)
    demo_user.stats.hearts = 1
    failed = answer(seeded_db, demo_user, attempt, attempt.exercises[0].id, is_correct=False)
    assert (failed.status, failed.hearts) == ("failed", 0)

    me = profile.refill_hearts(seeded_db, demo_user)
    assert me.stats.hearts == 5 and me.stats.gems == 1200 - REFILL_COST_GEMS
    assert seeded_db.get_one(LessonAttempt, attempt.attempt_id).status == "in_progress"


def test_match_pairs_mistake_costs_nothing(seeded_db: Session, demo_user: User) -> None:
    attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_at(seeded_db, 1, 4).id)
    match_exercise = next(item for item in attempt.exercises if item.type == "match_pairs")
    crossed = {"pairs": [], "mismatches": 2}
    response = lesson_engine.submit_answer(
        seeded_db, demo_user, attempt.attempt_id, match_exercise.id, crossed
    )
    assert not response.correct and response.hearts == 4
    assert seeded_db.get_one(LessonAttempt, attempt.attempt_id).mistakes == 0


def test_answer_guards(seeded_db: Session, demo_user: User) -> None:
    attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_at(seeded_db, 1, 4).id)
    first_id = attempt.exercises[0].id
    answer(seeded_db, demo_user, attempt, first_id, is_correct=True)

    with pytest.raises(AppError) as raised:
        answer(seeded_db, demo_user, attempt, first_id, is_correct=True)
    assert raised.value.code == "EXERCISE_ALREADY_CORRECT"

    exercise_from_another_lesson = seeded_db.scalars(
        select(Exercise.id).where(Exercise.lesson_id != attempt.lesson.id)
    ).first()
    assert exercise_from_another_lesson is not None
    with pytest.raises(AppError) as raised:
        lesson_engine.submit_answer(
            seeded_db, demo_user, attempt.attempt_id, exercise_from_another_lesson, {"text": "x"}
        )
    assert raised.value.code == "EXERCISE_NOT_IN_ATTEMPT"

    lesson_engine.quit_attempt(seeded_db, demo_user, attempt.attempt_id)
    with pytest.raises(AppError) as raised:
        answer(seeded_db, demo_user, attempt, attempt.exercises[1].id, is_correct=True)
    assert raised.value.code == "ATTEMPT_CLOSED"


def test_replaying_a_completed_skill_is_practice(seeded_db: Session, demo_user: User) -> None:
    skill_one = skill_at(seeded_db, 1, 1)
    attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_one.id)
    assert attempt.mode == "practice"
    result = play_correctly(seeded_db, demo_user, attempt).result
    assert result is not None and result.xp_earned == 15 and not result.skill_completed
    assert seeded_db.get_one(UserSkillProgress, (demo_user.id, skill_one.id)).lessons_completed == 3


def test_finishing_skill_four_unlocks_unit_two(seeded_db: Session, demo_user: User) -> None:
    skill_four = skill_at(seeded_db, 1, 4)
    for _ in range(2):
        attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_four.id)
        result = play_correctly(seeded_db, demo_user, attempt).result
    assert result is not None and result.skill_completed
    assert "scholar" in [unlock.code for unlock in result.achievements_unlocked]
    states = path.skill_states(seeded_db, demo_user)
    assert states[skill_four.id] == "completed"
    assert states[skill_at(seeded_db, 2, 1).id] == "active"


def test_leaderboard_lists_everyone_on_a_monday(seeded_db: Session, demo_user: User) -> None:
    today = clock.user_today(seeded_db, demo_user)
    days_to_next_monday = 7 - today.weekday()
    dev_tools.advance_day(seeded_db, demo_user, days_to_next_monday)

    board = leaderboard.get_weekly_leaderboard(seeded_db, demo_user)
    assert board.period_start == today + timedelta(days=days_to_next_monday)
    # Nobody has XP yet this week, and the LEFT JOIN still lists all 15 learners at 0.
    assert len(board.entries) == 15
    assert all(entry.xp == 0 for entry in board.entries)
    assert any(entry.is_me for entry in board.entries)
    # With everyone tied at 0, ties go alphabetically rather than to the lowest user id.
    names = [entry.display_name for entry in board.entries]
    assert names == sorted(names)


def test_simultaneous_completing_answers_award_once(
    seeded_db: Session, demo_user: User, engine: Engine
) -> None:
    """Session B plays 7 of 8 exercises; session A then completes the attempt and commits.
    B still holds the attempt as in progress, exactly like a request that read it a moment
    before A's commit, and submits the same completing answer."""
    attempt = lesson_engine.start_lesson(seeded_db, demo_user, skill_at(seeded_db, 1, 4).id)
    for exercise in attempt.exercises[:-1]:
        answer(seeded_db, demo_user, attempt, exercise.id, is_correct=True)
    last_exercise_id = attempt.exercises[-1].id

    with Session(engine, expire_on_commit=False) as other_request:
        winner = answer(
            other_request,
            other_request.get_one(User, DEMO_USER_ID),
            attempt,
            last_exercise_id,
            is_correct=True,
        )
    loser = answer(seeded_db, demo_user, attempt, last_exercise_id, is_correct=True)

    assert winner.result is not None and loser.result == winner.result
    with Session(engine) as check:
        stats = check.get_one(User, DEMO_USER_ID).stats
        today = check.get_one(DailyActivity, (DEMO_USER_ID, clock.user_today(check, demo_user)))
        answers_for_last = check.scalars(
            select(AttemptAnswer).where(
                AttemptAnswer.attempt_id == attempt.attempt_id,
                AttemptAnswer.exercise_id == last_exercise_id,
            )
        ).all()
    assert stats.total_xp == 115 + 15  # one perfect lesson, awarded once
    assert today.lessons_completed == 1
    assert len(answers_for_last) == 1  # the losing request's answer row was rolled back
