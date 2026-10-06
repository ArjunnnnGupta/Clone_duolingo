"""The learning path. Skill and unit states are derived from progress, never stored."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Course, Lesson, Skill, Unit, User, UserSkillProgress
from app.schemas.path import CourseOut, NodeState, PathResponse, SkillNode, UnitNode

LOCKED: NodeState = "locked"
ACTIVE: NodeState = "active"
COMPLETED: NodeState = "completed"


def lessons_completed_by_skill(db: Session, user: User) -> dict[int, int]:
    rows = db.execute(
        select(UserSkillProgress.skill_id, UserSkillProgress.lessons_completed).where(
            UserSkillProgress.user_id == user.id
        )
    )
    return {skill_id: completed for skill_id, completed in rows}


def lesson_count_by_skill(db: Session) -> dict[int, int]:
    rows = db.execute(select(Lesson.skill_id, func.count()).group_by(Lesson.skill_id))
    return {skill_id: count for skill_id, count in rows}


def skill_states(db: Session, user: User) -> dict[int, NodeState]:
    ordered_skill_ids = db.scalars(
        select(Skill.id)
        .join(Unit)
        .where(Unit.course_id == user.current_course_id)
        .order_by(Unit.position, Skill.position)
    )
    return _derive_states(
        list(ordered_skill_ids), lessons_completed_by_skill(db, user), lesson_count_by_skill(db)
    )


def _derive_states(
    ordered_skill_ids: list[int], completed_counts: dict[int, int], lesson_counts: dict[int, int]
) -> dict[int, NodeState]:
    """Walk the course in path order: finished skills are completed, the first unfinished
    one is active, and everything after it is locked."""
    states: dict[int, NodeState] = {}
    has_active_skill = False
    for skill_id in ordered_skill_ids:
        if completed_counts.get(skill_id, 0) >= lesson_counts[skill_id]:
            states[skill_id] = COMPLETED
        elif not has_active_skill:
            states[skill_id] = ACTIVE
            has_active_skill = True
        else:
            states[skill_id] = LOCKED
    return states


def get_path(db: Session, user: User) -> PathResponse:
    course = db.scalars(
        select(Course)
        .where(Course.id == user.current_course_id)
        .options(selectinload(Course.units).selectinload(Unit.skills))
    ).one()
    completed_counts = lessons_completed_by_skill(db, user)
    lesson_counts = lesson_count_by_skill(db)
    ordered_skill_ids = [skill.id for unit in course.units for skill in unit.skills]
    states = _derive_states(ordered_skill_ids, completed_counts, lesson_counts)
    units = []
    for unit in course.units:
        skills = [
            SkillNode(
                id=skill.id,
                title=skill.title,
                icon=skill.icon,
                state=states[skill.id],
                lessons_completed=completed_counts.get(skill.id, 0),
                lesson_count=lesson_counts[skill.id],
            )
            for skill in unit.skills
        ]
        units.append(_unit_node(unit, skills))
    return PathResponse(
        course=CourseOut(id=course.id, code=course.code, title=course.title), units=units
    )


def _unit_node(unit: Unit, skills: list[SkillNode]) -> UnitNode:
    # A unit is locked until its first skill opens, and completed once every skill is.
    if skills[0].state == LOCKED:
        state = LOCKED
    elif all(skill.state == COMPLETED for skill in skills):
        state = COMPLETED
    else:
        state = ACTIVE
    return UnitNode(
        id=unit.id,
        position=unit.position,
        title=unit.title,
        description=unit.description,
        color=unit.color,
        state=state,
        skills=skills,
    )
