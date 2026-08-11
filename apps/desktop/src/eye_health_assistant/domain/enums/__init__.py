"""Domain enums for timer and session management."""

from __future__ import annotations

from enum import Enum


class TimerPhase(Enum):
    """Current phase of the timer cycle."""

    FOCUS = "focus"
    BREAK = "break"
    LONG_BREAK = "long_break"


class SessionStatus(Enum):
    """Status of a monitoring session."""

    IDLE = "idle"
    FOCUSING = "focusing"
    FOCUS_PAUSED = "focus_paused"
    BREAK = "break"
    BREAK_PAUSED = "break_paused"
    COMPLETED = "completed"
    INTERRUPTED = "interrupted"


class SessionMode(Enum):
    """Mode of monitoring."""

    TIMER = "timer"
    SMART = "smart"
