"""Session repository for timer session persistence."""

from __future__ import annotations

import logging
from datetime import datetime

from eye_health_assistant.domain.enums import SessionMode, SessionStatus, TimerPhase
from eye_health_assistant.domain.models.timer_session import TimerSession
from eye_health_assistant.infrastructure.database.engine import Database
from eye_health_assistant.infrastructure.database.models import TimerSessionRow

logger = logging.getLogger(__name__)


class SessionRepository:
    """Repository for timer session CRUD operations."""

    def __init__(self, database: Database) -> None:
        self._db = database

    def save(self, session: TimerSession) -> None:
        """Save or update a timer session."""
        with self._db.get_session() as db_session:
            row = db_session.get(TimerSessionRow, session.id)
            if row is None:
                row = TimerSessionRow(id=session.id)
                db_session.add(row)

            row.mode = session.mode.value  # type: ignore[assignment]
            row.status = session.status.value  # type: ignore[assignment]
            row.phase = session.phase.value  # type: ignore[assignment]
            row.focus_duration = session.focus_duration  # type: ignore[assignment]
            row.break_duration = session.break_duration  # type: ignore[assignment]
            row.long_break_duration = session.long_break_duration  # type: ignore[assignment]
            row.sessions_until_long_break = session.sessions_until_long_break  # type: ignore[assignment]
            row.started_at = session.started_at  # type: ignore[assignment]
            row.ended_at = session.ended_at  # type: ignore[assignment]
            row.phase_started_at = session.phase_started_at  # type: ignore[assignment]
            row.completed_focus_sessions = session.completed_focus_sessions  # type: ignore[assignment]
            row.total_focus_seconds = session.current_focus_elapsed  # type: ignore[assignment]
            row.total_break_seconds = session.current_break_elapsed  # type: ignore[assignment]
            row.interrupted = 1 if session.status == SessionStatus.INTERRUPTED else 0  # type: ignore[assignment]
            row.content_version = session.content_version  # type: ignore[assignment]
            row.updated_at = datetime.utcnow()  # type: ignore[assignment]

            db_session.commit()

    def get_by_id(self, session_id: str) -> TimerSession | None:
        """Retrieve a session by ID."""
        with self._db.get_session() as db_session:
            row = db_session.get(TimerSessionRow, session_id)
            if row is None:
                return None
            return self._row_to_session(row)

    def get_recent(self, limit: int = 50) -> list[TimerSession]:
        """Get recent sessions ordered by creation date."""
        with self._db.get_session() as db_session:
            rows = (
                db_session.query(TimerSessionRow)
                .order_by(TimerSessionRow.created_at.desc())
                .limit(limit)
                .all()
            )
            return [self._row_to_session(r) for r in rows]

    def get_completed_today(self) -> list[TimerSession]:
        """Get all completed focus sessions from today."""
        today = datetime.utcnow().date()
        with self._db.get_session() as db_session:
            rows = (
                db_session.query(TimerSessionRow)
                .filter(
                    TimerSessionRow.ended_at.isnot(None),
                    TimerSessionRow.interrupted == 0,
                )
                .all()
            )
            return [
                self._row_to_session(r)
                for r in rows
                if r.ended_at and r.ended_at.date() == today
            ]

    def delete_all(self) -> int:
        """Delete all sessions. Returns count deleted."""
        with self._db.get_session() as db_session:
            count = db_session.query(TimerSessionRow).delete()
            db_session.commit()
            return count

    def delete(self, session_id: str) -> None:
        """Delete a session by ID."""
        with self._db.get_session() as db_session:
            row = db_session.get(TimerSessionRow, session_id)
            if row is not None:
                db_session.delete(row)
                db_session.commit()

    def get_today(self) -> list[TimerSession]:
        """Get all sessions from today."""
        today = datetime.utcnow().date()
        with self._db.get_session() as db_session:
            rows = (
                db_session.query(TimerSessionRow)
                .all()
            )
            return [
                self._row_to_session(r)
                for r in rows
                if r.started_at and r.started_at.date() == today
            ]

    def _row_to_session(self, row: TimerSessionRow) -> TimerSession:
        """Convert a database row to a domain model."""
        return TimerSession(
            id=str(row.id),
            mode=SessionMode(str(row.mode)),
            status=SessionStatus(str(row.status)),
            phase=TimerPhase(str(row.phase)),
            focus_duration=int(row.focus_duration),
            break_duration=int(row.break_duration),
            long_break_duration=int(row.long_break_duration),
            sessions_until_long_break=int(row.sessions_until_long_break),
            started_at=row.started_at if row.started_at else None,  # type: ignore[arg-type]
            ended_at=row.ended_at if row.ended_at else None,  # type: ignore[arg-type]
            phase_started_at=row.phase_started_at if row.phase_started_at else None,  # type: ignore[arg-type]
            completed_focus_sessions=int(row.completed_focus_sessions),
            current_focus_elapsed=float(row.total_focus_seconds),
            current_break_elapsed=float(row.total_break_seconds),
            content_version=str(row.content_version),
        )
