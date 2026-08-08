"""Dependency injection container."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from eye_health_assistant.app.lifecycle import ApplicationLifecycle
from eye_health_assistant.core.config import Config

logger = logging.getLogger(__name__)


@dataclass
class Dependencies:
    """Application dependency container.

    Manages shared application state and service instances.
    Services are lazily initialized on first access.
    """

    config: Config = field(default_factory=Config)
    lifecycle: ApplicationLifecycle | None = None

    def initialize(self) -> None:
        """Initialize all dependencies."""
        self.lifecycle = ApplicationLifecycle(self.config)
        self.lifecycle.initialize()
        logger.info("Dependencies initialized")

    def shutdown(self) -> None:
        """Shut down all dependencies."""
        if self.lifecycle:
            self.lifecycle.shutdown()
        logger.info("Dependencies shut down")
