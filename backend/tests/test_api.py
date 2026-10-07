"""The HTTP layer end to end: a whole lesson over the real routes, plus the error shapes."""

from datetime import date, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from app.config import Settings
from app.models import DailyActivity, Exercise, User
from app.seed.attempt_history import CORRECT_SUBMISSIONS, WRONG_SUBMISSIONS
from app.seed.run import DEMO_USER_ID, reset_database
from app.services import dev_tools
from app.services.hearts import REFILL_COST_GEMS

JSON = dict[str, Any]


def find_skill(path_body: JSON, title: str) -> JSON:
    return next(
        skill for unit in path_body["units"] for skill in unit["skills"] if skill["title"] == title
    )


def submission_for(engine: Engine, exercise_id: int, *, is_correct: bool) -> JSON:
    """Build an answer from the stored solution, the way a perfect (or wrong) client would."""
    builders = CORRECT_SUBMISSIONS if is_correct else WRONG_SUBMISSIONS
    with Session(engine) as session:
        exercise = session.get_one(Exercise, exercise_id)
        return builders[exercise.type](exercise)


def answer(
    client: TestClient, engine: Engine, attempt_id: int, exercise_id: int, *, is_correct: bool
) -> JSON:
    response = client.post(
        f"/api/attempts/{attempt_id}/answer",
        json={
            "exercise_id": exercise_id,
            "answer": submission_for(engine, exercise_id, is_correct=is_correct),
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def start_people_lesson(client: TestClient) -> JSON:
    path_body = client.get("/api/path").json()
    skill_four = find_skill(path_body, "People")
    assert (skill_four["state"], skill_four["lessons_completed"]) == ("active", 1)
    assert path_body["units"][1]["state"] == "locked"

    start = client.post("/api/lessons/start", json={"skill_id": skill_four["id"]})
    assert start.status_code == 200
    # Solutions must never reach the client, anywhere in the response.
    assert "solution" not in start.text
    return start.json()


def test_play_a_full_lesson_over_http(client: TestClient, engine: Engine) -> None:
    me = client.get("/api/me").json()
    assert (me["stats"]["hearts"], me["stats"]["total_xp"]) == (4, 115)
    assert (me["stats"]["current_streak"], me["daily"]["today_xp"]) == (6, 0)

    attempt = start_people_lesson(client)
    attempt_id, exercises = attempt["attempt_id"], attempt["exercises"]
    assert len(exercises) == 8 and attempt["hearts"] == 4 and attempt["status"] == "in_progress"

    wrong = answer(client, engine, attempt_id, exercises[0]["id"], is_correct=False)
    assert wrong["correct"] is False and wrong["hearts"] == 3 and wrong["correct_solution"]

    responses = [
        answer(client, engine, attempt_id, exercise["id"], is_correct=True)
        for exercise in exercises
    ]
    assert all(response["result"] is None for response in responses[:-1])
    completing = responses[-1]
    assert completing["status"] == "completed"
    result = completing["result"]
    assert (result["xp_earned"], result["mistakes"], result["accuracy"]) == (10, 1, 89)
    assert result["streak"] == {"count": 7, "extended": True}
    assert [unlock["code"] for unlock in result["achievements_unlocked"]] == ["wildfire"]

    assert_stored_result_is_stable(client, engine, attempt_id, exercises[-1]["id"], result)
    assert_state_after_lesson(client)


def test_me_exposes_the_countdown_refill_cost_and_week_strip(
    client: TestClient, engine: Engine
) -> None:
    me = client.get("/api/me").json()
    stats = me["stats"]
    assert stats["refill_cost_gems"] == REFILL_COST_GEMS
    assert 0 <= stats["seconds_until_next_heart"] <= 30 * 60  # 4 of 5 hearts, 30 min interval

    days = me["recent_days"]
    assert len(days) == 7
    dates = [date.fromisoformat(day["date"]) for day in days]
    assert dates == [dates[0] + timedelta(days=offset) for offset in range(7)]  # oldest first
    with Session(engine) as session:
        lessons_by_date = {
            row.activity_date: row.lessons_completed
            for row in session.scalars(select(DailyActivity).where(DailyActivity.user_id == 1))
        }
    for day_date, day in zip(dates, days, strict=True):
        assert day["is_active"] == (lessons_by_date.get(day_date, 0) > 0)
    # The demo learner has a 6-day streak that last ran yesterday: yesterday lit, today not yet.
    assert [day["is_active"] for day in days][-2:] == [True, False]


def test_week_strip_marks_today_after_a_lesson(client: TestClient, engine: Engine) -> None:
    attempt = start_people_lesson(client)
    for exercise in attempt["exercises"]:
        answer(client, engine, attempt["attempt_id"], exercise["id"], is_correct=True)

    days = client.get("/api/me").json()["recent_days"]
    assert days[-1]["is_active"] is True


def test_full_hearts_have_no_countdown(client: TestClient, engine: Engine) -> None:
    with Session(engine) as session:
        session.get_one(User, DEMO_USER_ID).stats.hearts = 5
        session.commit()
    assert client.get("/api/me").json()["stats"]["seconds_until_next_heart"] is None


def assert_stored_result_is_stable(
    client: TestClient, engine: Engine, attempt_id: int, last_exercise_id: int, result: JSON
) -> None:
    reloaded = client.get(f"/api/attempts/{attempt_id}").json()
    assert reloaded["status"] == "completed" and reloaded["result"] == result
    assert len(reloaded["answered"]) == 9  # 8 correct + 1 wrong
    replay = answer(client, engine, attempt_id, last_exercise_id, is_correct=True)
    assert replay["result"] == result


def assert_state_after_lesson(client: TestClient) -> None:
    after = client.get("/api/me").json()
    assert after["stats"]["total_xp"] == 125  # awarded once, despite the replayed answer
    assert (after["stats"]["hearts"], after["stats"]["current_streak"]) == (3, 7)
    assert after["daily"]["today_xp"] == 10
    assert find_skill(client.get("/api/path").json(), "People")["lessons_completed"] == 2


def test_progress_shows_up_on_profile_and_leaderboard(client: TestClient, engine: Engine) -> None:
    before = client.get("/api/leaderboard").json()
    assert len(before["entries"]) == 15
    skill_id = find_skill(client.get("/api/path").json(), "People")["id"]
    attempt = client.post("/api/lessons/start", json={"skill_id": skill_id}).json()
    for exercise in attempt["exercises"]:
        answer(client, engine, attempt["attempt_id"], exercise["id"], is_correct=True)

    after = client.get("/api/leaderboard").json()
    rank_before = next(entry["rank"] for entry in before["entries"] if entry["is_me"])
    rank_after = next(entry["rank"] for entry in after["entries"] if entry["is_me"])
    assert rank_after < rank_before
    profile = client.get("/api/me/profile").json()
    assert profile["stats"]["total_xp"] == 130 and len(profile["week_xp"]) == 7
    wildfire = next(
        item for item in client.get("/api/achievements").json() if item["code"] == "wildfire"
    )
    assert wildfire["unlocked_at"] is not None


def test_errors_use_the_documented_shape(client: TestClient) -> None:
    locked_skill = client.get("/api/path").json()["units"][1]["skills"][0]["id"]
    locked = client.post("/api/lessons/start", json={"skill_id": locked_skill})
    assert locked.status_code == 403
    assert locked.json()["error"]["code"] == "SKILL_LOCKED"

    missing = client.get("/api/attempts/99999")
    assert (missing.status_code, missing.json()["error"]["code"]) == (404, "NOT_FOUND")

    skill_id = client.get("/api/path").json()["units"][0]["skills"][3]["id"]
    attempt = client.post("/api/lessons/start", json={"skill_id": skill_id}).json()
    first_exercise = attempt["exercises"][0]["id"]
    bad_shape = client.post(
        f"/api/attempts/{attempt['attempt_id']}/answer",
        json={"exercise_id": first_exercise, "answer": {"tiles": ["x"]}},
    )
    assert (bad_shape.status_code, bad_shape.json()["error"]["code"]) == (400, "INVALID_ANSWER")

    quit_response = client.post(f"/api/attempts/{attempt['attempt_id']}/quit")
    assert quit_response.json() == {"status": "abandoned"}
    closed = client.post(
        f"/api/attempts/{attempt['attempt_id']}/answer",
        json={"exercise_id": first_exercise, "answer": {"option_id": "o1"}},
    )
    assert (closed.status_code, closed.json()["error"]["code"]) == (409, "ATTEMPT_CLOSED")


def test_hearts_endpoints(client: TestClient) -> None:
    refilled = client.post("/api/hearts/refill").json()
    assert refilled["stats"]["hearts"] == 5
    assert refilled["stats"]["gems"] == 1200 - REFILL_COST_GEMS
    full = client.post("/api/hearts/refill")
    assert (full.status_code, full.json()["error"]["code"]) == (409, "HEARTS_FULL")
    assert client.post("/api/hearts/practice").json()["stats"]["hearts"] == 5


def test_settings_update_and_validation(client: TestClient) -> None:
    updated = client.patch("/api/me/settings", json={"daily_goal_xp": 30, "display_name": "Sam"})
    assert updated.json()["daily"]["goal_xp"] == 30
    assert updated.json()["user"]["display_name"] == "Sam"
    invalid = client.patch("/api/me/settings", json={"daily_goal_xp": 25})
    # Same envelope as every other error, not FastAPI's default {"detail": [...]}.
    assert invalid.status_code == 422
    assert invalid.json()["error"]["code"] == "VALIDATION_ERROR"
    assert "daily_goal_xp" in invalid.json()["error"]["message"]


def test_dev_tools_advance_the_day_and_reset(client: TestClient) -> None:
    client.post("/api/dev/advance-day", json={"days": 2})
    # Two idle days break the 6-day streak, and the demo's yesterday-based goal resets.
    assert client.get("/api/me").json()["stats"]["current_streak"] == 0

    reset = client.post("/api/dev/reset").json()
    assert reset["stats"]["current_streak"] == 6 and reset["stats"]["total_xp"] == 115
    assert client.get("/api/me").json()["stats"]["current_streak"] == 6


def error_code(response: Any) -> tuple[int, str]:
    return response.status_code, response.json()["error"]["code"]


def test_no_hearts_blocks_a_start_over_http(client: TestClient, engine: Engine) -> None:
    skill_id = find_skill(client.get("/api/path").json(), "People")["id"]
    attempt = client.post("/api/lessons/start", json={"skill_id": skill_id}).json()
    heart_costing = [item["id"] for item in attempt["exercises"] if item["type"] != "match_pairs"]
    hearts_left = attempt["hearts"]
    for exercise_id in heart_costing[:hearts_left]:
        hearts_left = answer(client, engine, attempt["attempt_id"], exercise_id, is_correct=False)[
            "hearts"
        ]
    assert hearts_left == 0
    blocked = client.post("/api/lessons/start", json={"skill_id": skill_id})
    assert error_code(blocked) == (409, "NO_HEARTS")


def test_refill_without_enough_gems_over_http(client: TestClient, engine: Engine) -> None:
    with Session(engine) as session:
        stats = session.get_one(User, DEMO_USER_ID).stats
        stats.gems = REFILL_COST_GEMS - 1
        session.commit()
    assert error_code(client.post("/api/hearts/refill")) == (409, "NOT_ENOUGH_GEMS")


def test_answer_guards_over_http(client: TestClient, engine: Engine) -> None:
    skill_id = find_skill(client.get("/api/path").json(), "People")["id"]
    attempt = client.post("/api/lessons/start", json={"skill_id": skill_id}).json()
    attempt_id, first_exercise = attempt["attempt_id"], attempt["exercises"][0]["id"]
    answer(client, engine, attempt_id, first_exercise, is_correct=True)

    again = client.post(
        f"/api/attempts/{attempt_id}/answer",
        json={
            "exercise_id": first_exercise,
            "answer": submission_for(engine, first_exercise, is_correct=True),
        },
    )
    assert error_code(again) == (409, "EXERCISE_ALREADY_CORRECT")

    foreign = client.post(
        f"/api/attempts/{attempt_id}/answer",
        json={"exercise_id": exercise_outside(engine, attempt), "answer": {"text": "x"}},
    )
    assert error_code(foreign) == (400, "EXERCISE_NOT_IN_ATTEMPT")


def exercise_outside(engine: Engine, attempt: JSON) -> int:
    with Session(engine) as session:
        exercise_id = session.scalars(
            select(Exercise.id).where(Exercise.lesson_id != attempt["lesson"]["id"])
        ).first()
    assert exercise_id is not None
    return exercise_id


def test_reset_route_closes_the_session_before_resetting(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    open_connections: list[int] = []

    def spy_reset(target_engine: Engine) -> None:
        open_connections.append(target_engine.pool.checkedout())
        reset_database(target_engine)

    monkeypatch.setattr(dev_tools, "reset_database", spy_reset)
    client.post("/api/dev/advance-day", json={"days": 2})  # breaks the streak: 6 -> 0
    reset = client.post("/api/dev/reset").json()
    assert open_connections == [0]
    # A stale cached learner would still say 0 here; the reseeded one has 6.
    assert reset["stats"]["current_streak"] == 6


def test_achievements_show_an_expired_streak(client: TestClient) -> None:
    client.post("/api/dev/advance-day", json={"days": 2})
    wildfire = next(
        item for item in client.get("/api/achievements").json() if item["code"] == "wildfire"
    )
    assert wildfire["progress"] == 0


def test_dev_tools_are_off_unless_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ENABLE_DEV_TOOLS", raising=False)
    assert Settings(_env_file=None).enable_dev_tools is False
