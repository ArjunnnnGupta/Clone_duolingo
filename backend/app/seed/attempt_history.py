"""Answer rows and stored results for the demo learner's completed lessons."""

import random
from collections.abc import Callable
from datetime import datetime
from typing import Any, NamedTuple

from app.models import Achievement, AttemptAnswer, Exercise, LessonAttempt
from app.schemas.attempt_result import (
    AchievementUnlock,
    AttemptResult,
    DailyGoalResult,
    StreakResult,
)

Submission = dict[str, Any]
SubmissionBuilder = Callable[[Exercise], Submission]


def _correct_choice(exercise: Exercise) -> Submission:
    return {"option_id": exercise.solution["option_id"]}


def _correct_tiles(exercise: Exercise) -> Submission:
    return {"tiles": exercise.solution["accepted"][0]}


def _correct_pairs(exercise: Exercise) -> Submission:
    left_by_pair = {item["pair"]: item["id"] for item in exercise.payload["left"]}
    pairs = [[left_by_pair[item["pair"]], item["id"]] for item in exercise.payload["right"]]
    return {"pairs": pairs, "mismatches": 0}


def _correct_text(exercise: Exercise) -> Submission:
    return {"text": exercise.solution["accepted"][0]}


def _wrong_choice(exercise: Exercise) -> Submission:
    correct_id = exercise.solution["option_id"]
    wrong_option = next(
        option for option in exercise.payload["options"] if option["id"] != correct_id
    )
    return {"option_id": wrong_option["id"]}


def _wrong_tiles(exercise: Exercise) -> Submission:
    return {"tiles": list(reversed(exercise.solution["accepted"][0]))}


def _wrong_blank_option(exercise: Exercise) -> Submission:
    accepted = exercise.solution["accepted"]
    return {"text": next(word for word in exercise.payload["options"] if word not in accepted)}


def _wrong_text(_exercise: Exercise) -> Submission:
    return {"text": "???"}


# One builder per exercise type, the same registry pattern grading.py will use.
CORRECT_SUBMISSIONS: dict[str, SubmissionBuilder] = {
    "multiple_choice": _correct_choice,
    "translate": _correct_tiles,
    "match_pairs": _correct_pairs,
    "fill_blank": _correct_text,
    "type_answer": _correct_text,
}
# Match pairs is left out on purpose: it never costs a heart, so it is never a seeded mistake.
WRONG_SUBMISSIONS: dict[str, SubmissionBuilder] = {
    "multiple_choice": _wrong_choice,
    "translate": _wrong_tiles,
    "fill_blank": _wrong_blank_option,
    "type_answer": _wrong_text,
}


class PlannedAnswer(NamedTuple):
    exercise: Exercise
    is_correct: bool


def build_attempt_answers(
    randomizer: random.Random, attempt: LessonAttempt, *, finished_at: datetime
) -> list[AttemptAnswer]:
    """One correct row per exercise; each mistake adds a wrong row just before its correct one.

    Answer times are spread evenly from start to finish, so the last one lands on finished_at.
    """
    exercises = attempt.lesson.exercises
    mistake_candidates = [exercise for exercise in exercises if exercise.type in WRONG_SUBMISSIONS]
    mistaken = randomizer.sample(mistake_candidates, attempt.mistakes)
    planned: list[PlannedAnswer] = []
    for exercise in exercises:
        if exercise in mistaken:
            planned.append(PlannedAnswer(exercise, is_correct=False))
        planned.append(PlannedAnswer(exercise, is_correct=True))
    duration = finished_at - attempt.started_at
    return [
        AttemptAnswer(
            attempt=attempt,
            exercise=answer.exercise,
            submitted=_submission(answer.exercise, is_correct=answer.is_correct),
            is_correct=answer.is_correct,
            # Multiply before dividing so the last answer lands exactly on finished_at.
            answered_at=attempt.started_at + duration * number / len(planned),
        )
        for number, answer in enumerate(planned, start=1)
    ]


def _submission(exercise: Exercise, *, is_correct: bool) -> Submission:
    builders = CORRECT_SUBMISSIONS if is_correct else WRONG_SUBMISSIONS
    return builders[exercise.type](exercise)


def build_attempt_result(
    attempt: LessonAttempt,
    *,
    finished_at: datetime,
    streak_count: int,
    goal_xp: int,
    is_skill_completed: bool,
    unlocked: list[Achievement],
) -> dict[str, Any]:
    """The result as it would have been returned when the attempt was finalized.

    Each demo lesson was the only one done that day, so the streak always extended and the
    day's XP equals the lesson's XP.
    """
    exercise_count = len(attempt.lesson.exercises)
    result = AttemptResult(
        xp_earned=attempt.xp_earned,
        accuracy=round(100 * exercise_count / (exercise_count + attempt.mistakes)),
        mistakes=attempt.mistakes,
        duration_s=int((finished_at - attempt.started_at).total_seconds()),
        streak=StreakResult(count=streak_count, extended=True),
        daily_goal=DailyGoalResult(
            today_xp=attempt.xp_earned,
            goal_xp=goal_xp,
            just_met=attempt.xp_earned >= goal_xp,
        ),
        skill_completed=is_skill_completed,
        achievements_unlocked=[
            AchievementUnlock(code=item.code, title=item.title, icon=item.icon) for item in unlocked
        ],
    )
    return result.model_dump(mode="json")
