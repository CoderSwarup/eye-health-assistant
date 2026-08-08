"""Timer controller — orchestrates engine, persistence, and notifications."""

from __future__ import annotations

import logging
from collections.abc import Callable

from PySide6.QtCore import QObject, QTimer, Signal

from eye_health_assistant.domain.enums import SessionStatus
from eye_health_assistant.domain.models.timer_session import TimerSession
from eye_health_assistant.infrastructure.database.repository import SessionRepository
from eye_health_assistant.notifications.service import NotificationService
from eye_health_assistant.timer.engine import Clock, TimerEngine

logger = logging.getLogger(__name__)

# Update interval in milliseconds
TICK_INTERVAL_MS = 1000


class TimerController(QObject):
    """Qt-integrated timer controller.

    Signals:
        session_started: Emitted when a session begins.
        session_updated: Emitted every tick with updated session.
        session_paused: Emitted when paused.
        session_resumed: Emitted when resumed.
        focus_completed: Emitted when a focus period ends.
        break_completed: Emitted when a break ends.
        session_ended: Emitted when session stops or completes.
    """

    session_started = Signal()
    session_updated = Signal(object)
    session_paused = Signal()
    session_resumed = Signal()
    focus_completed = Signal()
    break_completed = Signal()
    session_ended = Signal(object)

    def __init__(
        self,
        repository: SessionRepository,
        notification_service: NotificationService,
        clock: Clock | None = None,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._engine = TimerEngine(clock=clock)
        self._repository = repository
        self._notifications = notification_service
        self._timer = QTimer(self)
        self._timer.setInterval(TICK_INTERVAL_MS)
        self._timer.timeout.connect(self._on_tick)
        self._on_focus_complete_cb: Callable[[], None] | None = None
        self._on_break_complete_cb: Callable[[], None] | None = None

    @property
    def session(self) -> TimerSession | None:
        return self._engine.session

    @property
    def is_running(self) -> bool:
        return self._engine.session is not None and self._engine.session.is_active

    @property
    def is_paused(self) -> bool:
        return self._engine.session is not None and self._engine.session.is_paused

    def set_on_focus_complete(self, callback: Callable[[], None]) -> None:
        """Set callback for when a focus period completes."""
        self._on_focus_complete_cb = callback

    def set_on_break_complete(self, callback: Callable[[], None]) -> None:
        """Set callback for when a break completes."""
        self._on_break_complete_cb = callback

    def start(
        self,
        focus_duration: int = 1200,
        break_duration: int = 20,
        long_break_duration: int = 300,
    ) -> None:
        """Start a new timer session."""
        session = self._engine.start(
            focus_duration=focus_duration,
            break_duration=break_duration,
            long_break_duration=long_break_duration,
        )
        self._repository.save(session)
        self._timer.start()
        self.session_started.emit()
        logger.info("Timer controller started session %s", session.id)

    def pause(self) -> None:
        """Pause the current session."""
        self._engine.pause()
        self._timer.stop()
        session = self._engine.session
        if session is not None:
            self._repository.save(session)
        self.session_paused.emit()

    def resume(self) -> None:
        """Resume a paused session."""
        self._engine.resume()
        self._timer.start()
        session = self._engine.session
        if session is not None:
            self._repository.save(session)
        self.session_resumed.emit()

    def stop(self) -> None:
        """Stop the current session."""
        session = self._engine.stop()
        self._timer.stop()
        self._repository.save(session)
        self.session_ended.emit(session)
        logger.info("Timer controller stopped session %s", session.id)

    def complete(self) -> None:
        """Complete the current session."""
        session = self._engine.complete()
        self._timer.stop()
        self._repository.save(session)
        self.session_ended.emit(session)

    def _on_tick(self) -> None:
        """Handle timer tick."""
        prev_status = self._engine.session.status if self._engine.session else None
        session = self._engine.tick()
        if session is None:
            return

        # Check for phase transitions
        focus_to_break = (
            prev_status == SessionStatus.FOCUSING
            and session.status == SessionStatus.BREAK
        )
        break_to_focus = (
            prev_status == SessionStatus.BREAK
            and session.status == SessionStatus.FOCUSING
        )
        if focus_to_break:
            self._on_focus_transition()
        elif break_to_focus:
            self._on_break_transition()

        self._repository.save(session)
        self.session_updated.emit(session)

    def _on_focus_transition(self) -> None:
        """Handle focus -> break transition."""
        self._notifications.notify_break_reminder()
        self.focus_completed.emit()
        if self._on_focus_complete_cb:
            self._on_focus_complete_cb()
        logger.info("Focus period completed, break started")

    def _on_break_transition(self) -> None:
        """Handle break -> focus transition."""
        self._notifications.notify_focus_complete()
        self.break_completed.emit()
        if self._on_break_complete_cb:
            self._on_break_complete_cb()
        logger.info("Break completed, next focus started")
