"""Weekly league table."""

import datetime as dt

from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    display_name: str
    avatar_color: str
    xp: int
    is_me: bool


class LeaderboardResponse(BaseModel):
    period_start: dt.date
    period_end: dt.date
    entries: list[LeaderboardEntry]
