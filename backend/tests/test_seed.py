import subprocess
import sys
from collections import Counter
from collections.abc import Iterator
from datetime import timedelta
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import create_db_engine
from app.models import (
    Achievement,
    AppSetting,
    AttemptAnswer,
    DailyActivity,
    Exercise,
    Lesson,
    LessonAttempt,
    Skill,
    Unit,
    User,
    UserSkillProgress,
    UserStats,
)
from app.models.content import EXERCISE_TYPES
from app.schemas.attempt_result import AttemptResult
from app.schemas.exercises import EXERCISE_ADAPTER
from app.seed.attempt_history import CORRECT_SUBMISSIONS, WRONG_SUBMISSIONS
from app.seed.run import DEMO_USER_ID, reset_database
from app.services import clock

EXPECTED_TYPE_COUNTS = {
    "multiple_choice": 72,
    "translate": 72,
    "match_pairs": 36,
    "fill_blank": 72,
    "type_answer": 36,
}
BACKEND_DIR = Path(__file__).resolve().parents[1]
# "I" and names keep their capitals mid-sentence, so they may appear capitalized as tiles.
ALWAYS_CAPITALIZED_WORDS = {"I", "Ana", "Monday", "Sunday"}
LESSON_EXERCISE_TYPES = [
    "multiple_choice",
    "match_pairs",
    "translate",
    "fill_blank",
    "multiple_choice",
    "translate",
    "fill_blank",
    "type_answer",
]


def seeded_session() -> Session:
    engine = create_db_engine("sqlite://")
    reset_database(engine)
    return Session(engine)


@pytest.fixture(scope="module")
def db() -> Iterator[Session]:
    session = seeded_session()
    yield session
    engine = session.get_bind()
    session.close()
    engine.dispose()


def count(db: Session, model: type) -> int:
    return db.scalar(select(func.count()).select_from(model)) or 0


def demo_attempts(db: Session) -> list[LessonAttempt]:
    return list(db.scalars(select(LessonAttempt).where(LessonAttempt.user_id == DEMO_USER_ID)))


def test_content_counts(db: Session) -> None:
    assert count(db, Unit) == 3
    assert count(db, Skill) == 12
    assert count(db, Lesson) == 36
    assert count(db, Exercise) == 288
    assert count(db, Achievement) == 5
    assert count(db, User) == 15


def test_exercise_type_totals(db: Session) -> None:
    types = Counter(db.scalars(select(Exercise.type)))
    assert dict(types) == EXPECTED_TYPE_COUNTS


def test_every_lesson_follows_the_position_table(db: Session) -> None:
    for lesson in db.scalars(select(Lesson)):
        assert [exercise.type for exercise in lesson.exercises] == LESSON_EXERCISE_TYPES


def test_every_stored_exercise_passes_the_union(db: Session) -> None:
    for exercise in db.scalars(select(Exercise)):
        EXERCISE_ADAPTER.validate_python(
            {
                "type": exercise.type,
                "prompt": exercise.prompt,
                "payload": exercise.payload,
                "solution": exercise.solution,
            }
        )


def test_demo_total_xp_equals_daily_activity(db: Session) -> None:
    stats = db.get(UserStats, DEMO_USER_ID)
    activity_xp = db.scalar(
        select(func.sum(DailyActivity.xp_earned)).where(DailyActivity.user_id == DEMO_USER_ID)
    )
    attempt_xp = db.scalar(
        select(func.sum(LessonAttempt.xp_earned)).where(LessonAttempt.user_id == DEMO_USER_ID)
    )
    assert stats is not None
    assert stats.total_xp == activity_xp == attempt_xp


def test_every_learner_total_matches_their_history(db: Session) -> None:
    for stats in db.scalars(select(UserStats)):
        activity_xp = db.scalar(
            select(func.coalesce(func.sum(DailyActivity.xp_earned), 0)).where(
                DailyActivity.user_id == stats.user_id
            )
        )
        assert stats.total_xp == activity_xp


def test_demo_learner_starting_state(db: Session) -> None:
    stats = db.get(UserStats, DEMO_USER_ID)
    assert stats is not None
    assert (stats.hearts, stats.gems) == (4, 1200)
    assert (stats.current_streak, stats.longest_streak) == (6, 9)
    assert stats.last_active_date == clock.today() - timedelta(days=1)
    attempts = demo_attempts(db)
    assert len(attempts) == 10
    assert sum(attempt.mistakes == 0 for attempt in attempts) == 3
    # Keyed by place in the course, not database id: unit 1 skills 1-3 done, skill 4 at 1/3.
    progress = {
        (row.skill.unit.position, row.skill.position): row.lessons_completed
        for row in db.scalars(
            select(UserSkillProgress).where(UserSkillProgress.user_id == DEMO_USER_ID)
        )
    }
    assert progress == {(1, 1): 3, (1, 2): 3, (1, 3): 3, (1, 4): 1}


def test_demo_learner_is_eighth_on_the_weekly_leaderboard(db: Session) -> None:
    if clock.today().weekday() == 0:
        pytest.skip("on a Monday the demo learner has no XP yet this week")
    week_start = clock.week_start(clock.today())
    rows = db.execute(
        select(DailyActivity.user_id, func.sum(DailyActivity.xp_earned))
        .where(DailyActivity.activity_date >= week_start)
        .group_by(DailyActivity.user_id)
        .order_by(func.sum(DailyActivity.xp_earned).desc())
    ).all()
    ranking = [user_id for user_id, _ in rows]
    weekly_xp = dict(rows)
    assert ranking.index(DEMO_USER_ID) == 7
    assert weekly_xp[ranking[6]] - weekly_xp[DEMO_USER_ID] == 10


def test_every_demo_attempt_has_a_correct_answer_per_exercise(db: Session) -> None:
    for attempt in demo_attempts(db):
        answers = list(
            db.scalars(
                select(AttemptAnswer)
                .where(AttemptAnswer.attempt_id == attempt.id)
                .order_by(AttemptAnswer.id)
            )
        )
        assert answers, f"attempt {attempt.id} has no answered rows"
        correct_ids = [answer.exercise_id for answer in answers if answer.is_correct]
        assert sorted(correct_ids) == sorted(exercise.id for exercise in attempt.lesson.exercises)
        assert sum(not answer.is_correct for answer in answers) == attempt.mistakes


def test_each_wrong_answer_is_followed_by_the_correct_one_for_that_exercise(db: Session) -> None:
    for attempt in demo_attempts(db):
        answers = attempt.answers
        for position, answer in enumerate(answers):
            if not answer.is_correct:
                following = answers[position + 1]
                assert following.is_correct and following.exercise_id == answer.exercise_id
                assert answer.exercise.type != "match_pairs"


def test_demo_attempts_store_a_valid_result(db: Session) -> None:
    for attempt in demo_attempts(db):
        assert attempt.result is not None
        result = AttemptResult.model_validate(attempt.result)
        assert result.xp_earned == attempt.xp_earned
        assert result.mistakes == attempt.mistakes


def test_answers_fall_between_start_and_finish(db: Session) -> None:
    for attempt in demo_attempts(db):
        answer_times = [answer.answered_at for answer in attempt.answers]
        assert attempt.finished_at is not None
        assert all(attempt.started_at < moment <= attempt.finished_at for moment in answer_times)
        assert answer_times[-1] == attempt.finished_at


def test_each_wrong_answer_differs_from_the_correct_one(db: Session) -> None:
    for attempt in demo_attempts(db):
        for position, answer in enumerate(attempt.answers):
            if not answer.is_correct:
                assert answer.submitted != attempt.answers[position + 1].submitted


def translate_exercises(db: Session) -> list[Exercise]:
    return list(db.scalars(select(Exercise).where(Exercise.type == "translate")))


def test_tile_bank_can_build_every_accepted_answer(db: Session) -> None:
    for exercise in translate_exercises(db):
        tiles = Counter(tile["text"] for tile in exercise.payload["tiles"])
        for answer in exercise.solution["accepted"]:
            assert not Counter(answer) - tiles, f"{answer} cannot be built from {tiles}"


def test_tile_capitals_do_not_reveal_the_first_word(db: Session) -> None:
    for exercise in translate_exercises(db):
        capitalized = {
            tile["text"] for tile in exercise.payload["tiles"] if tile["text"][0].isupper()
        }
        assert capitalized <= ALWAYS_CAPITALIZED_WORDS, exercise.payload["source_text"]


def test_fill_blank_has_exactly_one_correct_option(db: Session) -> None:
    for exercise in db.scalars(select(Exercise).where(Exercise.type == "fill_blank")):
        accepted = set(exercise.solution["accepted"])
        assert sum(option in accepted for option in exercise.payload["options"]) == 1


def test_submission_builders_cover_every_exercise_type() -> None:
    assert set(CORRECT_SUBMISSIONS) == set(EXERCISE_TYPES)
    # Match pairs never costs a heart, so it is the one type with no wrong-answer builder.
    assert set(WRONG_SUBMISSIONS) == set(EXERCISE_TYPES) - {"match_pairs"}


def test_day_offset_setting_is_zero(db: Session) -> None:
    setting = db.get(AppSetting, "day_offset")
    assert setting is not None
    assert setting.value == "0"


def test_generator_is_deterministic() -> None:
    def snapshot(session: Session) -> list[tuple[str, dict, dict]]:
        return [
            (exercise.prompt, exercise.payload, exercise.solution)
            for exercise in session.scalars(select(Exercise).order_by(Exercise.id))
        ]

    first, second = seeded_session(), seeded_session()
    assert snapshot(first) == snapshot(second)
    first.close()
    second.close()


def test_importing_the_seed_module_does_not_touch_the_real_database() -> None:
    # A fresh interpreter, because this test process has already imported app.db.
    check = "import sys, app.seed.run; sys.exit('app.db' in sys.modules)"
    completed = subprocess.run([sys.executable, "-c", check], cwd=BACKEND_DIR, check=False)
    assert completed.returncode == 0, "importing app.seed.run imported app.db"
