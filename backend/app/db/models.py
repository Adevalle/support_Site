from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

from .database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    added_by = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)