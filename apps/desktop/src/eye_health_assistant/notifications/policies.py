"""Notification policy — rate limiting, quiet hours, intelligent routing."""

from __future__ import annotations

import logging
from datetime import datetime, time
from enum import Enum
from typing import ClassVar

from eye_health_assistant.core.config import Config

logger = logging.getLogger(__name__)


class NotificationType(Enum):
    """Types of notifications the app can send."""

    BREAK_REMINDER = "break_reminder"
    FOCUS_COMPLETE = "focus_complete"
    SESSION_COMPLETE = "session_complete"
    BLINK_REMINDER = "blink_reminder"
    EXERCISE_SUGGESTION = "exercise_suggestion"


class NotificationPolicy:
    """Decides whether a notification should be sent.

    Enforces rate limiting, quiet hours, and per-type cooldowns.
    """

    # Minimum seconds between notifications of the same type
    _TYPE_COOLDOWNS: ClassVar[dict[NotificationType, float]] = {
        NotificationType.BREAK_REMINDER: 300,  # 5 min
        NotificationType.FOCUS_COMPLETE: 60,  # 1 min
        NotificationType.SESSION_COMPLETE: 60,  # 1 min
        NotificationType.BLINK_REMINDER: 600,  # 10 min
        NotificationType.EXERCISE_SUGGESTION: 1800,  # 30 min
    }

    def __init__(self, config: Config) -> None:
        self._config = config
        self._last_sent: dict[NotificationType, float] = {}
        self._last_any_sent: float = 0.0

    def should_send(self, notification_type: NotificationType) -> bool:
        """Check if a notification of this type should be sent now.

        Returns True if the notification passes all policy checks.
        """
        import time as _time

        now = _time.time()

        # Global disable
        if not self._config.notifications_enabled:
            return False

        # Quiet hours check
        if self._in_quiet_hours():
            logger.debug("Notification suppressed: quiet hours active")
            return False

        # Global rate limit (minimum interval between ANY notifications)
        global_min = self._config.min_notification_interval
        if now - self._last_any_sent < global_min:
            logger.debug(
                "Notification suppressed: global rate limit (%.0fs < %ds)",
                now - self._last_any_sent,
                global_min,
            )
            return False

        # Per-type cooldown
        cooldown = self._TYPE_COOLDOWNS.get(notification_type, 60)
        last_of_type = self._last_sent.get(notification_type, 0.0)
        if now - last_of_type < cooldown:
            logger.debug(
                "Notification suppressed: type cooldown for %s",
                notification_type.value,
            )
            return False

        return True

    def record_sent(self, notification_type: NotificationType) -> None:
        """Record that a notification was sent."""
        import time as _time

        now = _time.time()
        self._last_sent[notification_type] = now
        self._last_any_sent = now

    def _in_quiet_hours(self) -> bool:
        """Check if current time is within quiet hours."""
        if not hasattr(self._config, "quiet_hours_start"):
            return False

        try:
            now = datetime.now().time()
            start = time.fromisoformat(self._config.quiet_hours_start)
            end = time.fromisoformat(self._config.quiet_hours_end)

            if start <= end:
                # Same-day range (e.g., 22:00 - 07:00 is NOT same-day)
                return start <= now <= end
            else:
                # Overnight range (e.g., 22:00 - 07:00)
                return now >= start or now <= end
        except (ValueError, AttributeError):
            return False
