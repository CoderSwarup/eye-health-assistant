"""SQLAlchemy ORM models for persistent storage."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
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


class MonitoringSessionRow(Base):
    """Persisted smart monitoring session record."""

    __tablename__ = "monitoring_sessions"

    id: Column[str] = Column(String(36), primary_key=True)
    mode: Column[str] = Column(String(20), nullable=False, default="smart")
    status: Column[str] = Column(String(20), nullable=False, default="active")
    device_index: Column[int] = Column(Integer, nullable=False, default=0)

    started_at: Column[datetime | None] = Column(DateTime, nullable=True)  # type: ignore
    ended_at: Column[datetime | None] = Column(DateTime, nullable=True)  # type: ignore
    duration_seconds: Column[float] = Column(Float, nullable=False, default=0.0)

    total_blinks: Column[int] = Column(Integer, nullable=False, default=0)
    average_blink_rate: Column[float] = Column(Float, nullable=True)
    valid_observation_seconds: Column[float] = Column(
        Float, nullable=False, default=0.0
    )
    reminders_sent: Column[int] = Column(Integer, nullable=False, default=0)

    interrupted: Column[int] = Column(Integer, nullable=False, default=0)
    created_at: Column[datetime] = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Column[datetime] = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )


class BlinkMeasurementRow(Base):
    """Persisted blink measurement window record."""

    __tablename__ = "blink_measurements"

    id: Column[str] = Column(String(36), primary_key=True)
    session_id: Column[str] = Column(
        String(36), ForeignKey("monitoring_sessions.id"), nullable=False
    )
    window_start: Column[datetime] = Column(DateTime, nullable=False)
    window_end: Column[datetime] = Column(DateTime, nullable=False)

    blink_count: Column[int] = Column(Integer, nullable=False, default=0)
    estimated_blink_rate: Column[float] = Column(Float, nullable=True)
    valid_observation_seconds: Column[float] = Column(
        Float, nullable=False, default=0.0
    )
    algorithm_version: Column[str] = Column(
        String(10), nullable=False, default="1.0"
    )

    created_at: Column[datetime] = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )
