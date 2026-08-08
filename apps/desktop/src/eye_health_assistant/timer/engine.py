"""Timer engine — core countdown logic with state machine."""

from __future__ import annotations

import logging
import time
import uuid
from datetime import datetime
from typing import Protocol

from eye_health_assistant.domain.enums import SessionMode, SessionStatus, TimerPhase
from eye_health_assistant.domain.models.timer_session import TimerSession

logger = logging.getLogger(__name__)


class Clock(Protocol):
    """Clock abstraction for testability."""

    def now(self) -> float:
        """Return current monotonic time in seconds."""


class MonotonicClock:
    """Real monotonic clock."""

    def now(self) -> float:
        return time.monotonic()


class FakeClock:
    """Fake clock for testing."""

    def __init__(self, start: float = 0.0) -> None:
        self._time = start

    def now(self) -> float:
        return self._time

    def advance(self, seconds: float) -> None:
        """Advance the clock by given seconds."""
        self._time += seconds


class TimerEngine:
    """State machine driving the focus/break timer cycle.

    Transitions:
        IDLE -> FOCUSING (start)
        FOCUSING -> FOCUS_PAUSED (pause)
        FOCUS_PAUSED -> FOCUSING (resume)
        FOCUSING -> BREAK (focus complete)
        BREAK -> BREAK_PAUSED (pause)
        BREAK_PAUSED -> BREAK (resume)
        BREAK -> FOCUSING (break complete, auto-continue)
        FOCUSING -> INTERRUPTED (stop)
        BREAK -> INTERRUPTED (stop)
    """

    def __init__(self, clock: Clock | None = None) -> None:
        self._clock = clock or MonotonicClock()
        self._session: TimerSession | None = None
        self._last_tick: float | None = None

    @property
    def session(self) -> TimerSession | None:
        return self._session

    def start(
        self,
        focus_duration: int = 1200,
        break_duration: int = 20,
        long_break_duration: int = 300,
        sessions_until_long_break: int = 4,
    ) -> TimerSession:
        """Start a new focus session."""
        if self._session is not None and self._session.is_active:
            raise ValueError("Timer is already running")

        self._session = TimerSession(
            id=str(uuid.uuid4()),
            mode=SessionMode.TIMER,
            status=SessionStatus.FOCUSING,
            phase=TimerPhase.FOCUS,
            focus_duration=focus_duration,
            break_duration=break_duration,
            long_break_duration=long_break_duration,
            sessions_until_long_break=sessions_until_long_break,
            started_at=datetime.utcnow(),
            phase_started_at=datetime.utcnow(),
        )
        self._last_tick = self._clock.now()
        logger.info(
            "Timer started: focus=%ds, break=%ds", focus_duration, break_duration
        )
        return self._session

    def pause(self) -> None:
        """Pause the current session."""
        if self._session is None:
            raise ValueError("No active session")
        if self._session.status == SessionStatus.FOCUSING:
            self._session.status = SessionStatus.FOCUS_PAUSED
            self._session.paused_at = datetime.utcnow()
            logger.info("Timer paused (focus)")
        elif self._session.status == SessionStatus.BREAK:
            self._session.status = SessionStatus.BREAK_PAUSED
            self._session.paused_at = datetime.utcnow()
            logger.info("Timer paused (break)")
        else:
            raise ValueError(f"Cannot pause in state: {self._session.status}")

    def resume(self) -> None:
        """Resume a paused session."""
        if self._session is None:
            raise ValueError("No active session")
        if self._session.status == SessionStatus.FOCUS_PAUSED:
            self._session.status = SessionStatus.FOCUSING
            self._session.paused_at = None
            self._last_tick = self._clock.now()
            logger.info("Timer resumed (focus)")
        elif self._session.status == SessionStatus.BREAK_PAUSED:
            self._session.status = SessionStatus.BREAK
            self._session.paused_at = None
            self._last_tick = self._clock.now()
            logger.info("Timer resumed (break)")
        else:
            raise ValueError(f"Cannot resume in state: {self._session.status}")

    def stop(self) -> TimerSession:
        """Stop the current session and return it."""
        if self._session is None:
            raise ValueError("No active session")
        self._session.status = SessionStatus.INTERRUPTED
        self._session.ended_at = datetime.utcnow()
        logger.info(
            "Timer stopped: completed %d focus sessions",
            self._session.completed_focus_sessions,
        )
        session = self._session
        self._session = None
        self._last_tick = None
        return session

    def tick(self) -> TimerSession | None:
        """Process elapsed time. Returns the session if state changed.

        Call this on each timer interval (e.g., every 1000ms via QTimer).
        Returns the session with updated state, or None if no session.
        """
        if self._session is None or not self._session.is_active:
            return None

        now = self._clock.now()
        if self._last_tick is None:
            self._last_tick = now

        elapsed = now - self._last_tick
        self._last_tick = now

        if elapsed <= 0:
            return self._session

        if self._session.phase == TimerPhase.FOCUS:
            self._session.current_focus_elapsed += elapsed
            if self._session.focus_remaining <= 0:
                self._on_focus_complete()
        else:
            self._session.current_break_elapsed += elapsed
            if self._session.break_remaining <= 0:
                self._on_break_complete()

        return self._session

    def _on_focus_complete(self) -> None:
        """Handle focus period completion."""
        assert self._session is not None
        self._session.completed_focus_sessions += 1
        self._session.phase = TimerPhase.BREAK
        self._session.status = SessionStatus.BREAK
        self._session.current_break_elapsed = 0.0
        self._session.phase_started_at = datetime.utcnow()
        self._last_tick = self._clock.now()
        logger.info(
            "Focus complete: session %d, switching to break",
            self._session.completed_focus_sessions,
        )

    def _on_break_complete(self) -> None:
        """Handle break completion — auto-start next focus."""
        assert self._session is not None
        self._session.phase = TimerPhase.FOCUS
        self._session.status = SessionStatus.FOCUSING
        self._session.current_focus_elapsed = 0.0
        self._session.phase_started_at = datetime.utcnow()
        self._last_tick = self._clock.now()
        logger.info("Break complete, starting next focus session")

    def complete(self) -> TimerSession:
        """Mark the current session as completed."""
        if self._session is None:
            raise ValueError("No active session")
        self._session.status = SessionStatus.COMPLETED
        self._session.ended_at = datetime.utcnow()
        logger.info(
            "Session completed: %d focus sessions",
            self._session.completed_focus_sessions,
        )
        session = self._session
        self._session = None
        self._last_tick = None
        return session
