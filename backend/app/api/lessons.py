from fastapi import APIRouter

from app.deps import CurrentUser, DbSession
from app.schemas.lesson import (
    AnswerRequest,
    AnswerResponse,
    AttemptResponse,
    QuitResponse,
    StartLessonRequest,
)
from app.services import lesson_engine

router = APIRouter()


@router.post("/lessons/start")
def start_lesson(request: StartLessonRequest, db: DbSession, user: CurrentUser) -> AttemptResponse:
    return lesson_engine.start_lesson(db, user, request.skill_id)


@router.get("/attempts/{attempt_id}")
def get_attempt(attempt_id: int, db: DbSession, user: CurrentUser) -> AttemptResponse:
    return lesson_engine.get_attempt(db, user, attempt_id)


@router.post("/attempts/{attempt_id}/answer")
def submit_answer(
    attempt_id: int, request: AnswerRequest, db: DbSession, user: CurrentUser
) -> AnswerResponse:
    return lesson_engine.submit_answer(db, user, attempt_id, request.exercise_id, request.answer)


@router.post("/attempts/{attempt_id}/quit")
def quit_attempt(attempt_id: int, db: DbSession, user: CurrentUser) -> QuitResponse:
    return lesson_engine.quit_attempt(db, user, attempt_id)
