"""Tests for session repository persistence."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from eye_health_assistant.domain.enums import SessionMode, SessionStatus
from eye_health_assistant.domain.models.timer_session import TimerSession
from eye_health_assistant.infrastructure.database.engine import Database
from eye_health_assistant.infrastructure.database.repository import SessionRepository


@pytest.fixture
def db(tmp_path: Path) -> Database:
    """Create a temporary database."""
    db_path = tmp_path / "test.db"
    database = Database(db_path)
    database.initialize()
    yield database
    database.close()


@pytest.fixture
def repo(db: Database) -> SessionRepository:
    """Create a session repository."""
    return SessionRepository(db)


def _make_session(
    *,
    status: SessionStatus = SessionStatus.COMPLETED,
    mode: SessionMode = SessionMode.TIMER,
    started_at: datetime | None = None,
    focus_duration: int = 1200,
    completed_focus_sessions: int = 1,
) -> TimerSession:
    """Create a test session."""
    now = datetime.utcnow()
    return TimerSession(
        id=f"test-{now.timestamp()}",
        mode=mode,
        status=status,
        focus_duration=focus_duration,
        completed_focus_sessions=completed_focus_sessions,
        started_at=started_at or now,
        ended_at=now,
    )


class TestSessionRepository:
    """Test session persistence operations."""

    def test_save_and_get(self, repo: SessionRepository) -> None:
        """Save a session and retrieve it by ID."""
        session = _make_session()
        repo.save(session)

        retrieved = repo.get_by_id(session.id)
        assert retrieved is not None
        assert retrieved.id == session.id
        assert retrieved.mode == session.mode
        assert retrieved.status == session.status

    def test_get_nonexistent(self, repo: SessionRepository) -> None:
        """Getting a non-existent session returns None."""
        result = repo.get_by_id("nonexistent-id")
        assert result is None

    def test_get_recent(self, repo: SessionRepository) -> None:
        """get_recent returns sessions in reverse chronological order."""
        for i in range(5):
            session = _make_session(focus_duration=100 * i)
            session.started_at = datetime.utcnow() - timedelta(hours=i)
            repo.save(session)

        recent = repo.get_recent(limit=3)
        assert len(recent) == 3
        # Most recent first
        assert recent[0].focus_duration > recent[1].focus_duration

    def test_get_today(self, repo: SessionRepository) -> None:
        """get_today returns only today's sessions."""
        # Save today's session
        today_session = _make_session()
        today_session.started_at = datetime.utcnow()
        repo.save(today_session)

        # Save old session
        old_session = _make_session(focus_duration=200)
        old_session.started_at = datetime.utcnow() - timedelta(days=7)
        repo.save(old_session)

        today = repo.get_today()
        assert len(today) == 1
        assert today[0].id == today_session.id

    def test_delete(self, repo: SessionRepository) -> None:
        """Delete removes a session."""
        session = _make_session()
        repo.save(session)

        repo.delete(session.id)

        retrieved = repo.get_by_id(session.id)
        assert retrieved is None

    def test_delete_nonexistent(self, repo: SessionRepository) -> None:
        """Deleting a non-existent session does not raise."""
        repo.delete("nonexistent-id")  # Should not raise

    def test_save_updates_existing(self, repo: SessionRepository) -> None:
        """Saving with the same ID updates the existing session."""
        session = _make_session()
        repo.save(session)

        # Update the session
        session.status = SessionStatus.INTERRUPTED
        repo.save(session)

        retrieved = repo.get_by_id(session.id)
        assert retrieved is not None
        assert retrieved.status == SessionStatus.INTERRUPTED
