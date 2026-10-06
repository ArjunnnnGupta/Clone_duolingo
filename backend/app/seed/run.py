"""Drop, recreate and seed the database: `python -m app.seed.run`."""

import logging
import random
from collections import defaultdict
from datetime import date, datetime, time, timedelta

from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from app.models import (
    Achievement,
    AppSetting,
    Base,
    Course,
    DailyActivity,
    Exercise,
    Lesson,
    LessonAttempt,
    Skill,
    Unit,
    User,
    UserAchievement,
    UserSkillProgress,
    UserStats,
)
from app.models.content import DEFAULT_LESSON_XP, PERFECT_LESSON_BONUS_XP
from app.models.learner import DEFAULT_DAILY_GOAL_XP, MAX_HEARTS
from app.schemas.exercises import ExerciseDefinition
from app.seed import content
from app.seed.attempt_history import build_attempt_answers, build_attempt_result
from app.seed.generator import generate_skill_exercises
from app.services import clock

logger = logging.getLogger(__name__)

# Fixed seeds so every run produces the same demo history and the same rivals.
DEMO_HISTORY_SEED = 1001
RIVALS_SEED = 2002

DEMO_USER_ID = 1
DEMO_ACCOUNT_AGE_DAYS = 30
DEMO_HEARTS = 4
DEMO_GEMS = 1200
DEMO_HEARTS_AGE_MINUTES = 20
# Agreed deviation: the record streak predates the seeded window, so it is set, not computed.
DEMO_LONGEST_STREAK = 9
# Mistakes per completed lesson, oldest first: skills 1-3 in full, then lesson 1 of skill 4.
DEMO_LESSON_MISTAKES = (2, 0, 1, 3, 0, 1, 2, 1, 0, 2)
# Days before today on which each lesson was done. Days 6..1 form the current 6-day streak,
# day 7 is the one gap, days 11..8 are the earlier run.
DEMO_LESSON_DAYS_AGO = (11, 10, 9, 8, 6, 5, 4, 3, 2, 1)
DEMO_COMPLETED_SKILL_COUNT = 3
DEMO_LESSON_FINISH_TIME = time(18, 0)
DEMO_LESSON_DURATION = timedelta(minutes=8)

LEADERBOARD_MIN_WEEK_XP = 15
LEADERBOARD_MAX_WEEK_XP = 320
RIVALS_AHEAD_OF_DEMO = 7
RIVALS_BEHIND_DEMO = 7
# The learner just above the demo is this close, so one lesson visibly climbs the table.
NEXT_RIVAL_GAP_XP = 10
RIVAL_ACCOUNT_AGE_DAYS = range(30, 201)
RIVAL_GEM_AMOUNTS = range(100, 800, 50)

AVATAR_COLORS = ("green", "blue", "red", "orange", "gold", "purple")

OTHER_LEARNERS = (
    ("mateo", "Mateo Ruiz"),
    ("sofia", "Sofía Vega"),
    ("liam", "Liam Carter"),
    ("aiko", "Aiko Tanaka"),
    ("noor", "Noor Haddad"),
    ("lucas", "Lucas Meyer"),
    ("priya", "Priya Nair"),
    ("emma", "Emma Larsen"),
    ("diego", "Diego Torres"),
    ("zara", "Zara Ahmed"),
    ("jonas", "Jonas Weber"),
    ("mei", "Mei Chen"),
    ("omar", "Omar Haddad"),
    ("chloe", "Chloé Martin"),
)

ACHIEVEMENTS = (
    ("first_steps", "First Steps", "Complete your first lesson", "footprints", "lessons", 1),
    ("wildfire", "Wildfire", "Reach a 7 day streak", "flame", "streak", 7),
    ("sage", "Sage", "Earn 250 XP", "book", "total_xp", 250),
    ("scholar", "Scholar", "Complete 4 skills", "graduation-cap", "skills", 4),
    (
        "perfectionist",
        "Perfectionist",
        "Finish 5 lessons without a mistake",
        "target",
        "perfect_lessons",
        5,
    ),
)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Imported here, not at the top: app.db builds the real engine (and creates data/) as soon
    # as it is imported, and importing this module for its constants must not do that.
    from app.db import engine

    reset_database(engine)
    with Session(engine) as db:
        _log_summary(db)


def reset_database(target_engine: Engine) -> None:
    """Drop, recreate and seed every table on the given engine, in one transaction."""
    Base.metadata.drop_all(target_engine)
    Base.metadata.create_all(target_engine)
    with Session(target_engine) as db, db.begin():
        seed_database(db)


def seed_database(db: Session) -> None:
    """Fill an empty schema; the caller owns the transaction."""
    # Read the clock once so every seeded row agrees on what "now" and "today" are.
    now = clock.now()
    course = _seed_course(db)
    achievements = _seed_achievements(db)
    demo_week_xp = _seed_demo_learner(db, course, achievements, now)
    _seed_other_learners(db, course, demo_week_xp, now)
    db.add(AppSetting(key="day_offset", value="0"))


def _seed_course(db: Session) -> Course:
    units = [
        _build_unit(unit_position, unit_content)
        for unit_position, unit_content in enumerate(content.UNITS, start=1)
    ]
    course = Course(
        code=content.COURSE_CODE,
        title=content.COURSE_TITLE,
        learning_language=content.LEARNING_LANGUAGE,
        from_language=content.FROM_LANGUAGE,
        units=units,
    )
    db.add(course)
    # Flush now so the demo learner's queries below see the course and every row has its id,
    # rather than relying on a later query to trigger SQLAlchemy's automatic flush.
    db.flush()
    return course


def _build_unit(unit_position: int, unit_content: content.UnitContent) -> Unit:
    skills = [
        _build_skill(unit_position, skill_position, skill_content)
        for skill_position, skill_content in enumerate(unit_content.skills, start=1)
    ]
    return Unit(
        position=unit_position,
        title=f"Unit {unit_position}",
        description=unit_content.description,
        color=unit_content.color,
        skills=skills,
    )


def _build_skill(
    unit_position: int, skill_position: int, skill_content: content.SkillContent
) -> Skill:
    # Seeded by the skill's place in the course (unit 2, skill 3 -> 23), not its database id,
    # so the content stays identical even if ids are ever assigned differently. Only unique
    # while every unit has fewer than 10 skills.
    generator_seed = unit_position * 10 + skill_position
    lessons = [
        Lesson(
            position=lesson_position,
            xp_reward=DEFAULT_LESSON_XP,
            exercises=_build_exercises(exercises),
        )
        for lesson_position, exercises in enumerate(
            generate_skill_exercises(generator_seed, skill_content), start=1
        )
    ]
    return Skill(
        position=skill_position,
        title=skill_content.title,
        icon=skill_content.icon,
        lessons=lessons,
    )


def _build_exercises(exercises: list[ExerciseDefinition]) -> list[Exercise]:
    return [
        Exercise(
            position=position,
            type=exercise.type,
            prompt=exercise.prompt,
            payload=exercise.payload.model_dump(),
            solution=exercise.solution.model_dump(),
        )
        for position, exercise in enumerate(exercises, start=1)
    ]


def _seed_achievements(db: Session) -> dict[str, Achievement]:
    achievements = {
        code: Achievement(
            code=code,
            title=title,
            description=description,
            icon=icon,
            metric=metric,
            threshold=threshold,
        )
        for code, title, description, icon, metric, threshold in ACHIEVEMENTS
    }
    db.add_all(achievements.values())
    return achievements


def _seed_demo_learner(
    db: Session, course: Course, achievements: dict[str, Achievement], now: datetime
) -> int:
    """Create learner 1 with a believable history; returns their XP for the current week."""
    user = User(
        id=DEMO_USER_ID,
        username="alex",
        display_name="Alex Morgan",
        avatar_color="green",
        current_course=course,
        created_at=now - timedelta(days=DEMO_ACCOUNT_AGE_DAYS),
    )
    db.add(user)
    started_skills = _demo_started_skills(db)
    attempts = _seed_demo_attempts(
        db, user, _demo_completed_lessons(started_skills), achievements["first_steps"], now.date()
    )
    activity = _seed_demo_daily_activity(db, user, attempts)
    _seed_demo_skill_progress(db, user, started_skills, attempts)
    _seed_demo_stats(db, user, activity, now)
    db.add(
        UserAchievement(
            user=user,
            achievement=achievements["first_steps"],
            unlocked_at=attempts[0].finished_at,
        )
    )
    week_start = clock.week_start(now.date())
    return sum(row.xp_earned for row in activity if row.activity_date >= week_start)


def _demo_started_skills(db: Session) -> list[Skill]:
    """The completed skills plus the one in progress, in path order."""
    path_order = select(Skill).join(Unit).order_by(Unit.position, Skill.position)
    return list(db.scalars(path_order.limit(DEMO_COMPLETED_SKILL_COUNT + 1)))


def _demo_completed_lessons(started_skills: list[Skill]) -> list[Lesson]:
    *completed_skills, skill_in_progress = started_skills
    finished_in_full = [lesson for skill in completed_skills for lesson in skill.lessons]
    return finished_in_full + skill_in_progress.lessons[:1]


def _seed_demo_attempts(
    db: Session,
    user: User,
    lessons: list[Lesson],
    first_lesson_achievement: Achievement,
    today: date,
) -> list[LessonAttempt]:
    randomizer = random.Random(DEMO_HISTORY_SEED)
    lesson_days = [today - timedelta(days=days_ago) for days_ago in DEMO_LESSON_DAYS_AGO]
    active_days = set(lesson_days)
    attempts: list[LessonAttempt] = []
    for lesson, mistakes, lesson_day in zip(
        lessons, DEMO_LESSON_MISTAKES, lesson_days, strict=True
    ):
        finished_at = datetime.combine(lesson_day, DEMO_LESSON_FINISH_TIME)
        is_first_attempt = not attempts
        bonus_xp = PERFECT_LESSON_BONUS_XP if mistakes == 0 else 0
        attempt = LessonAttempt(
            user=user,
            lesson=lesson,
            mode="learn",
            status="completed",
            mistakes=mistakes,
            xp_earned=lesson.xp_reward + bonus_xp,
            started_at=finished_at - DEMO_LESSON_DURATION,
            finished_at=finished_at,
        )
        db.add(attempt)
        db.add_all(build_attempt_answers(randomizer, attempt, finished_at=finished_at))
        attempt.result = build_attempt_result(
            attempt,
            finished_at=finished_at,
            streak_count=_streak_ending_at(active_days, lesson_day),
            goal_xp=DEFAULT_DAILY_GOAL_XP,
            is_skill_completed=lesson.position == len(lesson.skill.lessons),
            unlocked=[first_lesson_achievement] if is_first_attempt else [],
        )
        attempts.append(attempt)
    return attempts


def _seed_demo_daily_activity(
    db: Session, user: User, attempts: list[LessonAttempt]
) -> list[DailyActivity]:
    """One row per active day, summed from that day's attempts so the totals always agree."""
    rows: dict[date, DailyActivity] = {}
    for attempt in attempts:
        day = attempt.started_at.date()
        if day not in rows:
            rows[day] = DailyActivity(
                user=user, activity_date=day, xp_earned=0, lessons_completed=0
            )
        row = rows[day]
        row.xp_earned += attempt.xp_earned
        row.lessons_completed += 1
    db.add_all(rows.values())
    return list(rows.values())


def _seed_demo_skill_progress(
    db: Session, user: User, skills: list[Skill], attempts: list[LessonAttempt]
) -> None:
    attempts_by_skill: dict[int, list[LessonAttempt]] = defaultdict(list)
    for attempt in attempts:
        attempts_by_skill[attempt.lesson.skill_id].append(attempt)
    for skill in skills:
        skill_attempts = attempts_by_skill[skill.id]
        last_finished_at = skill_attempts[-1].finished_at
        is_skill_complete = len(skill_attempts) == len(skill.lessons)
        db.add(
            UserSkillProgress(
                user=user,
                skill=skill,
                lessons_completed=len(skill_attempts),
                completed_at=last_finished_at if is_skill_complete else None,
                updated_at=last_finished_at,
            )
        )


def _seed_demo_stats(db: Session, user: User, activity: list[DailyActivity], now: datetime) -> None:
    active_days = {row.activity_date for row in activity}
    db.add(
        UserStats(
            user=user,
            total_xp=sum(row.xp_earned for row in activity),
            gems=DEMO_GEMS,
            hearts=DEMO_HEARTS,
            hearts_updated_at=now - timedelta(minutes=DEMO_HEARTS_AGE_MINUTES),
            current_streak=_streak_ending_at(active_days, now.date()),
            longest_streak=DEMO_LONGEST_STREAK,
            last_active_date=max(active_days),
        )
    )


def _seed_other_learners(db: Session, course: Course, demo_week_xp: int, now: datetime) -> None:
    randomizer = random.Random(RIVALS_SEED)
    today = now.date()
    week_xp_targets = _week_xp_targets(randomizer, demo_week_xp)
    for index, ((username, display_name), week_xp) in enumerate(
        zip(OTHER_LEARNERS, week_xp_targets, strict=True)
    ):
        user = User(
            username=username,
            display_name=display_name,
            avatar_color=AVATAR_COLORS[index % len(AVATAR_COLORS)],
            current_course=course,
            created_at=now - timedelta(days=randomizer.choice(RIVAL_ACCOUNT_AGE_DAYS)),
        )
        activity = _week_activity(randomizer, user, week_xp, today)
        db.add_all(activity)
        active_days = {row.activity_date for row in activity}
        streak = _streak_ending_at(active_days, today)
        db.add(
            UserStats(
                user=user,
                total_xp=sum(row.xp_earned for row in activity),
                gems=randomizer.choice(RIVAL_GEM_AMOUNTS),
                hearts=MAX_HEARTS,
                hearts_updated_at=now,
                current_streak=streak,
                longest_streak=streak,
                last_active_date=max(active_days, default=None),
            )
        )


def _week_xp_targets(randomizer: random.Random, demo_week_xp: int) -> list[int]:
    """Weekly XP for the 14 rivals, highest first, placing the demo learner 8th."""
    seventh_place_xp = demo_week_xp + NEXT_RIVAL_GAP_XP
    top_six = randomizer.sample(
        range(seventh_place_xp + 1, LEADERBOARD_MAX_WEEK_XP + 1), RIVALS_AHEAD_OF_DEMO - 1
    )
    ahead = sorted(top_six, reverse=True) + [seventh_place_xp]
    return ahead + _evenly_below(demo_week_xp, RIVALS_BEHIND_DEMO)


def _evenly_below(demo_week_xp: int, count: int) -> list[int]:
    """`count` XP values spread evenly under the demo learner's, highest first.

    They start at the usual 15 XP floor when there is room. Early in the week the demo has
    less than that, so they start at 0 instead (agreed deviation from the 15 XP floor).
    """
    has_room_above_floor = demo_week_xp > LEADERBOARD_MIN_WEEK_XP + count
    floor = LEADERBOARD_MIN_WEEK_XP if has_room_above_floor else 0
    step = (demo_week_xp - floor) / (count + 1)
    return [floor + round(step * position) for position in range(count, 0, -1)]


def _week_activity(
    randomizer: random.Random, user: User, week_xp: int, today: date
) -> list[DailyActivity]:
    """Split a week's XP evenly over a few random days between Monday and today."""
    if week_xp == 0:
        return []
    week_start = clock.week_start(today)
    days_so_far = [
        week_start + timedelta(days=offset) for offset in range((today - week_start).days + 1)
    ]
    day_count = min(randomizer.randint(1, len(days_so_far)), week_xp)
    active_days = sorted(randomizer.sample(days_so_far, day_count))
    # Equal shares; the last day takes the remainder so the days add up to week_xp exactly.
    share, remainder = divmod(week_xp, day_count)
    amounts = [share] * (day_count - 1) + [share + remainder]
    return [
        DailyActivity(
            user=user,
            activity_date=day,
            xp_earned=amount,
            lessons_completed=max(1, round(amount / DEFAULT_LESSON_XP)),
        )
        for day, amount in zip(active_days, amounts, strict=True)
    ]


def _streak_ending_at(active_days: set[date], day: date) -> int:
    """Consecutive active days counting back from `day`.

    A streak is still alive on the day after the last active one, so an inactive `day`
    counts back from the day before it.
    """
    current = day if day in active_days else day - timedelta(days=1)
    streak = 0
    while current in active_days:
        streak += 1
        current -= timedelta(days=1)
    return streak


def _log_summary(db: Session) -> None:
    for model in (Unit, Skill, Lesson, Exercise, User, Achievement):
        logger.info(
            "%s: %d", model.__tablename__, db.scalar(select(func.count()).select_from(model))
        )
    total_xp = db.scalar(select(UserStats.total_xp).where(UserStats.user_id == DEMO_USER_ID))
    activity_xp = db.scalar(
        select(func.sum(DailyActivity.xp_earned)).where(DailyActivity.user_id == DEMO_USER_ID)
    )
    logger.info("demo total_xp=%s, sum(daily_activity)=%s", total_xp, activity_xp)


if __name__ == "__main__":
    main()
