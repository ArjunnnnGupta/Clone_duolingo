"""Dev-tools requests."""

from pydantic import BaseModel, Field


class AdvanceDayRequest(BaseModel):
    days: int = Field(default=1, ge=1, le=30)
