"""Tests for the timer engine state machine."""

from __future__ import annotations

import pytest

from eye_health_assistant.domain.enums import SessionStatus, TimerPhase
from eye_health_assistant.timer.engine import FakeClock, TimerEngine


class TestTimerEngineStateMachine:
    """Test timer engine state transitions."""

    def setup_method(self) -> None:
        self.clock = FakeClock(0.0)
        self.engine = TimerEngine(clock=self.clock)

    def test_start_creates_session(self) -> None:
        """Starting creates a new session in FOCUSING state."""
        session = self.engine.start(focus_duration=60, break_duration=10)
        assert session.status == SessionStatus.FOCUSING
        assert session.phase == TimerPhase.FOCUS
        assert session.focus_duration == 60
        assert session.break_duration == 10

    def test_start_while_running_raises(self) -> None:
        """Cannot start a new session while one is running."""
        self.engine.start()
        with pytest.raises(ValueError, match="already running"):
            self.engine.start()

    def test_pause_focus(self) -> None:
        """Pausing during focus transitions to FOCUS_PAUSED."""
        self.engine.start(focus_duration=60)
        self.engine.pause()
        assert self.engine.session is not None
        assert self.engine.session.status == SessionStatus.FOCUS_PAUSED

    def test_pause_break(self) -> None:
        """Pausing during break transitions to BREAK_PAUSED."""
        self.engine.start(focus_duration=1, break_duration=10)
        # Complete focus
        self.clock.advance(1.0)
        self.engine.tick()
        assert self.engine.session is not None
        assert self.engine.session.status == SessionStatus.BREAK

        self.engine.pause()
        assert self.engine.session.status == SessionStatus.BREAK_PAUSED

    def test_pause_idle_raises(self) -> None:
        """Cannot pause when no session is active."""
        with pytest.raises(ValueError, match="No active session"):
            self.engine.pause()

    def test_resume_focus(self) -> None:
        """Resuming from pause returns to FOCUSING."""
        self.engine.start(focus_duration=60)
        self.engine.pause()
        self.engine.resume()
        assert self.engine.session is not None
        assert self.engine.session.status == SessionStatus.FOCUSING

    def test_resume_break(self) -> None:
        """Resuming from break pause returns to BREAK."""
        self.engine.start(focus_duration=1, break_duration=10)
        self.clock.advance(1.0)
        self.engine.tick()
        self.engine.pause()
        self.engine.resume()
        assert self.engine.session is not None
        assert self.engine.session.status == SessionStatus.BREAK

    def test_resume_idle_raises(self) -> None:
        """Cannot resume when no session is active."""
        with pytest.raises(ValueError, match="No active session"):
            self.engine.resume()

    def test_stop_returns_session(self) -> None:
        """Stopping returns the session with INTERRUPTED status."""
        self.engine.start(focus_duration=60)
        session = self.engine.stop()
        assert session.status == SessionStatus.INTERRUPTED
        assert session.ended_at is not None
        assert self.engine.session is None

    def test_stop_idle_raises(self) -> None:
        """Cannot stop when no session is active."""
        with pytest.raises(ValueError, match="No active session"):
            self.engine.stop()

    def test_tick_focus_completes(self) -> None:
        """Tick advances focus time; completing focus switches to BREAK."""
        self.engine.start(focus_duration=10, break_duration=5)
        self.clock.advance(10.0)
        session = self.engine.tick()
        assert session is not None
        assert session.phase == TimerPhase.BREAK
        assert session.status == SessionStatus.BREAK
        assert session.completed_focus_sessions == 1

    def test_tick_break_completes(self) -> None:
        """Tick advances break time; completing break switches back to FOCUS."""
        self.engine.start(focus_duration=10, break_duration=5)
        # Complete focus
        self.clock.advance(10.0)
        self.engine.tick()
        # Complete break
        self.clock.advance(5.0)
        session = self.engine.tick()
        assert session is not None
        assert session.phase == TimerPhase.FOCUS
        assert session.status == SessionStatus.FOCUSING
        assert session.current_focus_elapsed == 0.0

    def test_tick_no_session(self) -> None:
        """Tick with no session returns None."""
        result = self.engine.tick()
        assert result is None

    def test_progress_calculation(self) -> None:
        """Progress reflects elapsed time as a percentage."""
        self.engine.start(focus_duration=100)
        self.clock.advance(50.0)
        session = self.engine.tick()
        assert session is not None
        assert 45.0 <= session.progress <= 55.0

    def test_focus_remaining(self) -> None:
        """focus_remaining decreases as time passes."""
        self.engine.start(focus_duration=100)
        self.clock.advance(30.0)
        session = self.engine.tick()
        assert session is not None
        assert 65.0 <= session.focus_remaining <= 75.0

    def test_break_remaining(self) -> None:
        """break_remaining decreases during break phase."""
        self.engine.start(focus_duration=10, break_duration=20)
        self.clock.advance(10.0)
        self.engine.tick()  # Switch to break
        self.clock.advance(5.0)
        session = self.engine.tick()
        assert session is not None
        assert 10.0 <= session.break_remaining <= 20.0

    def test_multiple_focus_sessions(self) -> None:
        """Multiple focus sessions increment completed_focus_sessions."""
        self.engine.start(focus_duration=5, break_duration=2)
        for _ in range(3):
            self.clock.advance(5.0)
            self.engine.tick()  # Complete focus
            self.clock.advance(2.0)
            self.engine.tick()  # Complete break

        assert self.engine.session is not None
        assert self.engine.session.completed_focus_sessions == 3

    def test_complete_session(self) -> None:
        """complete() marks session as COMPLETED."""
        self.engine.start(focus_duration=60)
        session = self.engine.complete()
        assert session.status == SessionStatus.COMPLETED
        assert session.ended_at is not None
        assert self.engine.session is None
