"""Database engine and session management."""

from __future__ import annotations

import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from eye_health_assistant.infrastructure.database.models import Base

logger = logging.getLogger(__name__)


class Database:
    """SQLite database connection manager."""

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._engine = create_engine(
            f"sqlite:///{db_path}",
            echo=False,
            connect_args={"check_same_thread": False},
        )
        self._session_factory = sessionmaker(bind=self._engine)

    def initialize(self) -> None:
        """Create all tables if they do not exist."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        Base.metadata.create_all(self._engine)
        logger.info("Database initialized at %s", self._db_path)

    def get_session(self) -> Session:
        """Create a new database session."""
        return self._session_factory()

    def close(self) -> None:
        """Dispose of the engine."""
        self._engine.dispose()
        logger.info("Database connection closed")
