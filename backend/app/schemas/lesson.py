"""Lesson start, attempt state and answer submission."""

from typing import Any, Literal

from pydantic import BaseModel

from app.schemas.attempt_result import AttemptResult
from app.schemas.exercises import ExercisePublic

AttemptMode = Literal["learn", "practice"]
AttemptStatus = Literal["in_progress", "completed", "failed", "abandoned"]


class StartLessonRequest(BaseModel):
    skill_id: int


class LessonInfo(BaseModel):
    id: int
    position: int
    skill_title: str


class AnsweredExercise(BaseModel):
    exercise_id: int
    is_correct: bool


class AttemptResponse(BaseModel):
    """Returned by start and by GET, so a refresh rebuilds the player from the same shape."""

    attempt_id: int
    mode: AttemptMode
    status: AttemptStatus
    lesson: LessonInfo
    exercises: list[ExercisePublic]
    hearts: int
    answered: list[AnsweredExercise]
    result: AttemptResult | None


class AnswerRequest(BaseModel):
    exercise_id: int
    # Validated against the exercise's own answer model in grading.py.
    answer: dict[str, Any]


class AnswerResponse(BaseModel):
    correct: bool
    correct_solution: str | None
    feedback_note: str | None
    hearts: int
    status: AttemptStatus
    result: AttemptResult | None


class QuitResponse(BaseModel):
    status: AttemptStatus
