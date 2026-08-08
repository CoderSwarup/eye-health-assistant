"""Timer session domain model."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from eye_health_assistant.domain.enums import SessionMode, SessionStatus, TimerPhase


@dataclass
class TimerSession:
    """A timer monitoring session."""

    id: str = ""
    mode: SessionMode = SessionMode.TIMER
    status: SessionStatus = SessionStatus.IDLE
    phase: TimerPhase = TimerPhase.FOCUS

    # Configuration
    focus_duration: int = 1200  # seconds
    break_duration: int = 20  # seconds
    long_break_duration: int = 300  # seconds
    sessions_until_long_break: int = 4

    # Timing
    started_at: datetime | None = None
    ended_at: datetime | None = None
    phase_started_at: datetime | None = None
    paused_at: datetime | None = None
    total_paused_duration: float = 0.0  # seconds

    # Progress
    completed_focus_sessions: int = 0
    current_focus_elapsed: float = 0.0
    current_break_elapsed: float = 0.0

    # Metadata
    content_version: str = "1.0"

    @property
    def is_active(self) -> bool:
        """Whether the session is currently running (not paused)."""
        return self.status in (
            SessionStatus.FOCUSING,
            SessionStatus.BREAK,
        )

    @property
    def is_paused(self) -> bool:
        """Whether the session is paused."""
        return self.status in (
            SessionStatus.FOCUS_PAUSED,
            SessionStatus.BREAK_PAUSED,
        )

    @property
    def focus_remaining(self) -> float:
        """Remaining focus time in seconds."""
        return max(0.0, self.focus_duration - self.current_focus_elapsed)

    @property
    def break_remaining(self) -> float:
        """Remaining break time in seconds."""
        duration = (
            self.long_break_duration
            if self._is_long_break
            else self.break_duration
        )
        return max(0.0, duration - self.current_break_elapsed)

    @property
    def _is_long_break(self) -> bool:
        """Whether the next break should be a long break."""
        return (
            self.completed_focus_sessions > 0
            and self.completed_focus_sessions % self.sessions_until_long_break == 0
        )

    @property
    def current_duration(self) -> int:
        """Duration of the current phase in seconds."""
        if self.phase == TimerPhase.FOCUS:
            return self.focus_duration
        if self._is_long_break:
            return self.long_break_duration
        return self.break_duration

    @property
    def current_remaining(self) -> float:
        """Remaining time in the current phase."""
        if self.phase == TimerPhase.FOCUS:
            return self.focus_remaining
        return self.break_remaining

    @property
    def current_elapsed(self) -> float:
        """Elapsed time in the current phase."""
        if self.phase == TimerPhase.FOCUS:
            return self.current_focus_elapsed
        return self.current_break_elapsed

    @property
    def progress(self) -> float:
        """Progress of the current phase as a percentage (0-100)."""
        duration = self.current_duration
        if duration <= 0:
            return 0.0
        elapsed = self.current_elapsed
        return min(100.0, (elapsed / duration) * 100.0)
