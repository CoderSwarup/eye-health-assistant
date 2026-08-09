"""Application bootstrap and lifecycle management."""

from __future__ import annotations

import logging

from eye_health_assistant.core.config import Config
from eye_health_assistant.core.constants import VERSION
from eye_health_assistant.core.logging import setup_logging
from eye_health_assistant.infrastructure.database.engine import Database

logger = logging.getLogger(__name__)


class ApplicationLifecycle:
    """Manages application startup and shutdown."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._initialized = False
        self.database: Database | None = None

    def initialize(self) -> None:
        """Initialize application components."""
        if self._initialized:
            return

        logger.info("Initializing Eye Health Assistant v%s", VERSION)

        # Set up logging first
        log_dir = self.config.app_data_dir / "logs"
        setup_logging(level=self.config.log_level, log_dir=log_dir)

        # Ensure directories exist
        self._ensure_directories()

        # Initialize database using config path
        self._init_database()

        self._initialized = True
        logger.info("Application initialized successfully")

    def _init_database(self) -> None:
        """Initialize the SQLite database."""
        db_path = self.config.database_path
        if db_path is None:
            db_path = self.config.app_data_dir / "database" / "app.sqlite"
            self.config.database_path = db_path

        db_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            self.database = Database(db_path)
            self.database.initialize()
            logger.info("Database initialized at %s", db_path)
        except Exception as e:
            logger.critical("Failed to initialize database: %s", e)
            raise

    def _ensure_directories(self) -> None:
        """Ensure required application directories exist."""
        directories = [
            self.config.app_data_dir / "database",
            self.config.app_data_dir / "logs",
            self.config.app_data_dir / "exports",
            self.config.app_data_dir / "cache",
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def shutdown(self) -> None:
        """Clean up application resources."""
        if not self._initialized:
            return

        logger.info("Shutting down Eye Health Assistant")

        if self.database:
            try:
                self.database.close()
            except Exception as e:
                logger.error("Error closing database: %s", e)

        self._initialized = False
        logger.info("Shutdown complete")
