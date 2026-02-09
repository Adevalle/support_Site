from pydantic import BaseModel
from datetime import datetime


class TrackCreate(BaseModel):
    title: str
    url: str
    added_by: str | None = None


class TrackOut(BaseModel):
    id: int
    title: str
    url: str
    added_at: datetime
    added_by: str | None
    is_active: bool

    class Config:
        from_attributes = True