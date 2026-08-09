"""Notification service — desktop notifications for timer events."""

from __future__ import annotations

import logging

from eye_health_assistant.core.config import Config

logger = logging.getLogger(__name__)


class NotificationService:
    """Desktop notification delivery service."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def notify_break_reminder(self) -> None:
        """Send a notification that it's time for a break."""
        if not self._config.notifications_enabled:
            return
        self._send(
            "Time for a Break",
            "Look away from your screen and give your eyes a moment.",
        )

    def notify_focus_complete(self) -> None:
        """Send a notification that a focus session completed."""
        if not self._config.notifications_enabled:
            return
        self._send(
            "Break Complete",
            "Ready for another focus session?",
        )

    def notify_session_complete(self, focus_count: int) -> None:
        """Send a notification that the entire session completed."""
        if not self._config.notifications_enabled:
            return
        self._send(
            "Session Complete",
            f"You completed {focus_count} focus session"
            + ("s" if focus_count != 1 else "")
            + ". Great work!",
        )

    def notify_blink_reminder(self) -> None:
        """Send a gentle reminder about low blink rate."""
        if not self._config.notifications_enabled:
            return
        self._send(
            "Eye Wellness Reminder",
            "You've been focused for a while. "
            "Try a few relaxed blinks or take a short visual break.",
        )

    def _send(self, title: str, message: str) -> None:
        """Send a desktop notification."""
        logger.info("Notification: %s — %s", title, message)
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
