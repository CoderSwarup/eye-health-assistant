"""Database migration system — lightweight versioned migrations."""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy import Column, Integer, String, text
from sqlalchemy.orm import Session

from eye_health_assistant.infrastructure.database.models import Base

logger = logging.getLogger(__name__)

# Current schema version — increment when adding a migration
SCHEMA_VERSION = 1


class SchemaVersionRow(Base):
    """Tracks the current database schema version."""

    __tablename__ = "schema_version"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, nullable=False)
    applied_at = Column(String, nullable=False)


def _ensure_version_table(session: Session) -> None:
    """Create the schema_version table if it doesn't exist."""
    session.execute(
        text(
            "CREATE TABLE IF NOT EXISTS schema_version "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "version INTEGER NOT NULL, "
            "applied_at TEXT NOT NULL)"
        )
    )
    session.commit()


def get_current_version(session: Session) -> int:
    """Get the current schema version from the database."""
    _ensure_version_table(session)
    result = session.execute(text("SELECT MAX(version) FROM schema_version"))
    row = result.fetchone()
    if row and row[0] is not None:
        return int(row[0])
    return 0


def apply_migrations(session: Session) -> None:
    """Apply all pending migrations up to SCHEMA_VERSION."""
    _ensure_version_table(session)
    current = get_current_version(session)

    if current >= SCHEMA_VERSION:
        logger.info("Database schema is up to date (version %d)", current)
        return

    logger.info(
        "Migrating database from version %d to %d", current, SCHEMA_VERSION
    )

    # Apply migrations in order
    migrations = _get_migrations()
    for version in range(current + 1, SCHEMA_VERSION + 1):
        if version in migrations:
            logger.info("Applying migration v%d", version)
            migrations[version](session)
            session.execute(
                text(
                    "INSERT INTO schema_version (version, applied_at) "
                    "VALUES (:version, :applied_at)"
                ),
                {
                    "version": version,
                    "applied_at": datetime.now(UTC).isoformat(),
                },
            )
            session.commit()
            logger.info("Migration v%d applied successfully", version)

    logger.info("Database schema is now at version %d", SCHEMA_VERSION)


def _get_migrations() -> dict[int, Callable[[Session], None]]:
    """Return a dict of version -> migration function."""
    return {
        1: _migration_v1,
    }


def _migration_v1(session: Session) -> None:
    """Initial schema — create all tables.

    This migration exists so future migrations have a starting point.
    Tables are created via create_all() in the engine, so this migration
    is a no-op but establishes the version tracking system.
    """
    pass
