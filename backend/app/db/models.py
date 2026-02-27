from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    url = Column(String, nullable=False)
    yandex_track_id = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    added_by = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
    admin_id = Column(Integer, ForeignKey("admins.telegram_id"), nullable=False)
    admin = relationship("Admin", back_populates="tracks")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)

    tracks = relationship("Track", back_populates="admin")
