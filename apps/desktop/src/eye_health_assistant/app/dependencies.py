"""Dependency injection container."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import QObject

from eye_health_assistant.analytics.service import AnalyticsService
from eye_health_assistant.app.lifecycle import ApplicationLifecycle
from eye_health_assistant.core.config import Config, get_app_data_dir
from eye_health_assistant.infrastructure.database.monitoring_repository import (
    MonitoringRepository,
)
from eye_health_assistant.infrastructure.database.repository import SessionRepository
from eye_health_assistant.monitoring.service import MonitoringService
from eye_health_assistant.notifications.service import NotificationService
from eye_health_assistant.timer.controller import TimerController

logger = logging.getLogger(__name__)

CONFIG_FILENAME = "config.json"


@dataclass
class Dependencies:
    """Application dependency container.

    Manages shared application state and service instances.
    Services are lazily initialized on first access.
    """

    config: Config = field(default_factory=Config)
    config_path: Path = field(
        default_factory=lambda: get_app_data_dir() / CONFIG_FILENAME
    )
    lifecycle: ApplicationLifecycle | None = None
    session_repository: SessionRepository | None = None
    monitoring_repository: MonitoringRepository | None = None
    notification_service: NotificationService | None = None
    timer_controller: TimerController | None = None
    monitoring_service: MonitoringService | None = None
    analytics_service: AnalyticsService | None = None

    def initialize(self, parent: QObject | None = None) -> None:
        """Initialize all dependencies."""
        # Load config from file (falls back to defaults on error)
        self.config = Config.from_file(self.config_path)

        self.lifecycle = ApplicationLifecycle(self.config)
        self.lifecycle.initialize()

        # Create repositories
        if self.lifecycle.database:
            self.session_repository = SessionRepository(
                self.lifecycle.database
            )
            self.monitoring_repository = MonitoringRepository(
                self.lifecycle.database
            )
            self.analytics_service = AnalyticsService(
                self.lifecycle.database
            )

        # Create services
        self.notification_service = NotificationService(self.config)

        # Create monitoring service
        if self.notification_service:
            self.monitoring_service = MonitoringService(
                config=self.config,
                notification_service=self.notification_service,
                parent=parent,
            )

        # Create controllers
        if self.session_repository and self.notification_service:
            self.timer_controller = TimerController(
                repository=self.session_repository,
                notification_service=self.notification_service,
                parent=parent,
            )

        logger.info("Dependencies initialized")

    def save_config(self) -> list[str]:
        """Validate and save the current config to disk.

        Returns list of validation errors (empty if successful).
        """
        errors = self.config.validate()
        if errors:
            logger.warning("Config validation failed: %s", "; ".join(errors))
            return errors

        try:
            self.config.save(self.config_path)
            logger.info("Config saved to %s", self.config_path)
        except OSError as e:
            logger.error("Failed to save config: %s", e)
            return [f"Failed to save: {e}"]

        return []

    def shutdown(self) -> None:
        """Shut down all dependencies."""
        if self.monitoring_service and self.monitoring_service.is_active:
            self.monitoring_service.stop()
        if self.timer_controller and self.timer_controller.is_running:
            self.timer_controller.stop()
        if self.lifecycle:
            self.lifecycle.shutdown()
        logger.info("Dependencies shut down")
