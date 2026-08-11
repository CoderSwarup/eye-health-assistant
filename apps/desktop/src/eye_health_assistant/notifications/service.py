"""Notification service — desktop notifications for timer events."""

from __future__ import annotations

import logging

from eye_health_assistant.core.config import Config
from eye_health_assistant.notifications.policies import (
    NotificationPolicy,
    NotificationType,
)

logger = logging.getLogger(__name__)


class NotificationService:
    """Desktop notification delivery service."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._policy = NotificationPolicy(config)

    def notify_break_reminder(self) -> None:
        """Send a notification that it's time for a break."""
        if not self._policy.should_send(NotificationType.BREAK_REMINDER):
            return
        self._send(
            NotificationType.BREAK_REMINDER,
            "Time for a Break",
            "Look away from your screen and give your eyes a moment.",
        )

    def notify_focus_complete(self) -> None:
        """Send a notification that a focus session completed."""
        if not self._policy.should_send(NotificationType.FOCUS_COMPLETE):
            return
        self._send(
            NotificationType.FOCUS_COMPLETE,
            "Break Complete",
            "Ready for another focus session?",
        )

    def notify_session_complete(self, focus_count: int) -> None:
        """Send a notification that the entire session completed."""
        if not self._policy.should_send(NotificationType.SESSION_COMPLETE):
            return
        self._send(
            NotificationType.SESSION_COMPLETE,
            "Session Complete",
            f"You completed {focus_count} focus session"
            + ("s" if focus_count != 1 else "")
            + ". Great work!",
        )

    def notify_blink_reminder(self) -> None:
        """Send a gentle reminder about low blink rate."""
        if not self._policy.should_send(NotificationType.BLINK_REMINDER):
            return
        self._send(
            NotificationType.BLINK_REMINDER,
            "Eye Wellness Reminder",
            "You've been focused for a while. "
            "Try a few relaxed blinks or take a short visual break.",
        )

    def notify_exercise_suggestion(self) -> None:
        """Send a suggestion to try an exercise."""
        if not self._policy.should_send(NotificationType.EXERCISE_SUGGESTION):
            return
        self._send(
            NotificationType.EXERCISE_SUGGESTION,
            "Exercise Suggestion",
            "Consider a short eye exercise to reduce screen fatigue.",
        )

    def _send(
        self,
        notification_type: NotificationType,
        title: str,
        message: str,
    ) -> None:
        """Send a desktop notification through the policy layer."""
        logger.info("Notification: %s — %s", title, message)
        self._policy.record_sent(notification_type)
        try:
            self._send_desktop(title, message)
        except Exception:
            logger.exception("Failed to send notification")

    def _send_desktop(self, title: str, message: str) -> None:
        """Send a platform-native desktop notification.

        Uses QSystemTrayIcon if available, otherwise logs only.
        """
        from PySide6.QtWidgets import QApplication, QSystemTrayIcon

        app = QApplication.instance()
        if app is None or not isinstance(app, QApplication):
            return

        tray = None
        for widget in app.topLevelWidgets():
            if isinstance(widget, QSystemTrayIcon):
                tray = widget
                break

        if tray is not None and tray.isVisible():
            icon = QSystemTrayIcon.MessageIcon.Information
            tray.showMessage(title, message, icon, 5000)
        else:
            # Fallback: just log when tray is not available
            logger.info("Notification (no tray): %s — %s", title, message)
