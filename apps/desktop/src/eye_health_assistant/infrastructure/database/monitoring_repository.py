"""Monitoring repository — persistence for smart monitoring sessions."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime

from eye_health_assistant.infrastructure.database.engine import Database
from eye_health_assistant.infrastructure.database.models import (
    BlinkMeasurementRow,
    MonitoringSessionRow,
)

logger = logging.getLogger(__name__)


class MonitoringRepository:
    """Repository for monitoring session and blink measurement CRUD."""

    def __init__(self, database: Database) -> None:
        self._db = database

    def create_session(
        self,
        device_index: int = 0,
    ) -> str:
        """Create a new monitoring session and return its ID."""
        session_id = str(uuid.uuid4())
        with self._db.get_session() as db_session:
            row = MonitoringSessionRow(
                id=session_id,
                mode="smart",
                status="active",
                device_index=device_index,
                started_at=datetime.utcnow(),
            )
            db_session.add(row)
            db_session.commit()
        logger.info("Monitoring session created: %s", session_id)
        return session_id

    def end_session(
        self,
        session_id: str,
        *,
        total_blinks: int = 0,
        average_blink_rate: float | None = None,
        valid_observation_seconds: float = 0.0,
        reminders_sent: int = 0,
        interrupted: bool = False,
    ) -> None:
        """End a monitoring session with summary metrics."""
        with self._db.get_session() as db_session:
            row = db_session.get(MonitoringSessionRow, session_id)
            if row is None:
                logger.warning("Session not found: %s", session_id)
                return

            row.ended_at = datetime.utcnow()  # type: ignore[assignment]
            if row.started_at:
                row.duration_seconds = (row.ended_at - row.started_at).total_seconds()
            row.total_blinks = total_blinks  # type: ignore[assignment]
            row.average_blink_rate = average_blink_rate  # type: ignore[assignment]
            row.valid_observation_seconds = valid_observation_seconds  # type: ignore[assignment]
            row.reminders_sent = reminders_sent  # type: ignore[assignment]
            row.interrupted = 1 if interrupted else 0  # type: ignore[assignment]
            row.status = "completed" if not interrupted else "interrupted"  # type: ignore[assignment]
            row.updated_at = datetime.utcnow()  # type: ignore[assignment]
            db_session.commit()
        logger.info("Monitoring session ended: %s", session_id)

    def add_measurement(
        self,
        session_id: str,
        *,
        window_start: datetime,
        window_end: datetime,
        blink_count: int,
        estimated_blink_rate: float | None,
        valid_observation_seconds: float,
        algorithm_version: str = "1.0",
    ) -> str:
        """Add a blink measurement window. Returns the measurement ID."""
        measurement_id = str(uuid.uuid4())
        with self._db.get_session() as db_session:
            row = BlinkMeasurementRow(
                id=measurement_id,
                session_id=session_id,
                window_start=window_start,
                window_end=window_end,
                blink_count=blink_count,
                estimated_blink_rate=estimated_blink_rate,
                valid_observation_seconds=valid_observation_seconds,
                algorithm_version=algorithm_version,
            )
            db_session.add(row)
            db_session.commit()
        return measurement_id

    def get_recent_sessions(self, limit: int = 20) -> list[MonitoringSessionRow]:
        """Get recent monitoring sessions."""
        with self._db.get_session() as db_session:
            return (
                db_session.query(MonitoringSessionRow)
                .order_by(MonitoringSessionRow.created_at.desc())
                .limit(limit)
                .all()
            )

    def get_session_measurements(
        self, session_id: str
    ) -> list[BlinkMeasurementRow]:
        """Get all blink measurements for a session."""
        with self._db.get_session() as db_session:
            return (
                db_session.query(BlinkMeasurementRow)
                .filter(BlinkMeasurementRow.session_id == session_id)
                .order_by(BlinkMeasurementRow.window_start)
                .all()
            )

    def delete_all(self) -> int:
        """Delete all monitoring data. Returns count deleted."""
        with self._db.get_session() as db_session:
            count = db_session.query(BlinkMeasurementRow).delete()
            count += db_session.query(MonitoringSessionRow).delete()
            db_session.commit()
            return count
