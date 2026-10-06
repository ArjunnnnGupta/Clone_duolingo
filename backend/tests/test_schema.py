from collections.abc import Iterator
from datetime import datetime

import pytest
from sqlalchemy import func, inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import Base, create_db_engine
from app.models import Course, Exercise, Lesson, Skill, Unit, User, UserStats

EXPECTED_TABLES = {
    "courses",
    "units",
    "skills",
    "lessons",
    "exercises",
    "users",
    "user_stats",
    "user_skill_progress",
    "daily_activity",
    "achievements",
    "user_achievements",
    "app_settings",
    "lesson_attempts",
    "attempt_answers",
}
FIXED_TIME = datetime(2026, 1, 1, 12, 0)


@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_db_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as db_session:
        yield db_session
    engine.dispose()


def make_course() -> Course:
    return Course(code="es-en", title="Spanish", learning_language="es", from_language="en")


def make_course_tree() -> Course:
    exercise = Exercise(
        position=1,
        type="multiple_choice",
        prompt="Pick 'water'",
        payload={"options": ["agua", "pan"]},
        solution={"answer": "agua"},
    )
    lesson = Lesson(position=1, exercises=[exercise])
    skill = Skill(position=1, title="Greetings", icon="wave", lessons=[lesson])
    unit = Unit(position=1, title="Basics", description="Start", color="green", skills=[skill])
    course = make_course()
    course.units = [unit]
    return course


def test_create_all_builds_all_14_tables(session: Session) -> None:
    table_names = set(inspect(session.get_bind()).get_table_names())
    assert table_names == EXPECTED_TABLES


def test_foreign_key_to_missing_row_is_rejected(session: Session) -> None:
    session.add(Unit(course_id=999, position=1, title="Orphan", description="", color="green"))
    with pytest.raises(IntegrityError):
        session.flush()


def test_unknown_exercise_type_is_rejected(session: Session) -> None:
    course = make_course_tree()
    session.add(course)
    session.flush()
    lesson_id = course.units[0].skills[0].lessons[0].id
    session.add(
        Exercise(
            lesson_id=lesson_id, position=2, type="essay", prompt="?", payload={}, solution={}
        )
    )
    with pytest.raises(IntegrityError):
        session.flush()


def test_hearts_above_maximum_are_rejected(session: Session) -> None:
    course = make_course()
    user = User(
        username="learner",
        display_name="Learner",
        avatar_color="blue",
        current_course=course,
        created_at=FIXED_TIME,
    )
    user.stats = UserStats(hearts=6, hearts_updated_at=FIXED_TIME)
    session.add(user)
    with pytest.raises(IntegrityError):
        session.flush()


def test_deleting_course_cascades_to_content(session: Session) -> None:
    session.add(make_course_tree())
    session.commit()

    session.delete(session.scalars(select(Course)).one())
    session.commit()

    for model in (Unit, Skill, Lesson, Exercise):
        assert session.scalar(select(func.count()).select_from(model)) == 0
