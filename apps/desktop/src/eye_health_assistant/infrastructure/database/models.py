"""SQLAlchemy ORM models for persistent storage."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class TimerSessionRow(Base):
    """Persisted timer session record."""

    __tablename__ = "timer_sessions"

    id: Column[str] = Column(String(36), primary_key=True)
    mode: Column[str] = Column(String(20), nullable=False, default="timer")
    status: Column[str] = Column(String(20), nullable=False, default="idle")
    phase: Column[str] = Column(String(20), nullable=False, default="focus")

    focus_duration: Column[int] = Column(Integer, nullable=False, default=1200)
    break_duration: Column[int] = Column(Integer, nullable=False, default=20)
    long_break_duration: Column[int] = Column(Integer, nullable=False, default=300)
    sessions_until_long_break: Column[int] = Column(
        Integer, nullable=False, default=4
    )

    started_at: Column[datetime | None] = Column(DateTime, nullable=True)  # type: ignore
    ended_at: Column[datetime | None] = Column(DateTime, nullable=True)  # type: ignore
    phase_started_at: Column[datetime | None] = Column(DateTime, nullable=True)  # type: ignore

    completed_focus_sessions: Column[int] = Column(
        Integer, nullable=False, default=0
    )
    total_focus_seconds: Column[float] = Column(
        Float, nullable=False, default=0.0
    )
    total_break_seconds: Column[float] = Column(
        Float, nullable=False, default=0.0
    )

    interrupted: Column[int] = Column(Integer, nullable=False, default=0)
    content_version: Column[str] = Column(
        String(10), nullable=False, default="1.0"
    )
    created_at: Column[datetime] = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Column[datetime] = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    def to_dict(self) -> dict:
        """Convert to dictionary for domain model reconstruction."""
        return {
            "id": self.id,
            "mode": self.mode,
            "status": self.status,
            "phase": self.phase,
            "focus_duration": self.focus_duration,
            "break_duration": self.break_duration,
            "long_break_duration": self.long_break_duration,
            "sessions_until_long_break": self.sessions_until_long_break,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "phase_started_at": self.phase_started_at,
            "completed_focus_sessions": self.completed_focus_sessions,
            "total_focus_seconds": self.total_focus_seconds,
            "total_break_seconds": self.total_break_seconds,
            "interrupted": self.interrupted,
            "content_version": self.content_version,
        }
