"""The learning path: units and skills with their derived state."""

from typing import Literal

from pydantic import BaseModel

NodeState = Literal["locked", "active", "completed"]


class SkillNode(BaseModel):
    id: int
    title: str
    icon: str
    state: NodeState
    lessons_completed: int
    lesson_count: int


class UnitNode(BaseModel):
    id: int
    position: int
    title: str
    description: str
    color: str
    state: NodeState
    skills: list[SkillNode]


class CourseOut(BaseModel):
    id: int
    code: str
    title: str


class PathResponse(BaseModel):
    course: CourseOut
    units: list[UnitNode]
