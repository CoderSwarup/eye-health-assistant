"""Dependency injection container."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from PySide6.QtCore import QObject

from eye_health_assistant.app.lifecycle import ApplicationLifecycle
from eye_health_assistant.core.config import Config
from eye_health_assistant.infrastructure.database.repository import SessionRepository
from eye_health_assistant.notifications.service import NotificationService
from eye_health_assistant.timer.controller import TimerController

logger = logging.getLogger(__name__)


@dataclass
class Dependencies:
    """Application dependency container.

    Manages shared application state and service instances.
    Services are lazily initialized on first access.
    """

    config: Config = field(default_factory=Config)
    lifecycle: ApplicationLifecycle | None = None
    session_repository: SessionRepository | None = None
    notification_service: NotificationService | None = None
    timer_controller: TimerController | None = None

    def initialize(self, parent: QObject | None = None) -> None:
        """Initialize all dependencies."""
        self.lifecycle = ApplicationLifecycle(self.config)
        self.lifecycle.initialize()

        # Create repositories
        if self.lifecycle.database:
            self.session_repository = SessionRepository(
                self.lifecycle.database
            )

        # Create services
        self.notification_service = NotificationService(self.config)

        # Create controllers
        if self.session_repository and self.notification_service:
            self.timer_controller = TimerController(
                repository=self.session_repository,
                notification_service=self.notification_service,
                parent=parent,
            )

        logger.info("Dependencies initialized")

    def shutdown(self) -> None:
        """Shut down all dependencies."""
        if self.timer_controller and self.timer_controller.is_running:
            self.timer_controller.stop()
        if self.lifecycle:
            self.lifecycle.shutdown()
        logger.info("Dependencies shut down")
