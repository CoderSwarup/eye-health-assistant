"""Tests for monitoring repository persistence."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from eye_health_assistant.infrastructure.database.engine import Database
from eye_health_assistant.infrastructure.database.monitoring_repository import (
    MonitoringRepository,
)


@pytest.fixture
def db(tmp_path: Path) -> Database:
    db_path = tmp_path / "test_monitoring.db"
    database = Database(db_path)
    database.initialize()
    yield database
    database.close()


@pytest.fixture
def repo(db: Database) -> MonitoringRepository:
    return MonitoringRepository(db)


class TestMonitoringRepository:
    """Test monitoring session and measurement persistence."""

    def test_create_session(self, repo: MonitoringRepository) -> None:
        """Should create a session and return its ID."""
        session_id = repo.create_session(device_index=1)
        assert session_id is not None
        assert len(session_id) > 0

    def test_end_session(self, repo: MonitoringRepository) -> None:
        """Should end a session with summary metrics."""
        session_id = repo.create_session()
        repo.end_session(
            session_id,
            total_blinks=42,
            average_blink_rate=18.5,
            valid_observation_seconds=300.0,
            reminders_sent=2,
        )
        sessions = repo.get_recent_sessions()
        assert len(sessions) == 1
        assert sessions[0].total_blinks == 42
        assert sessions[0].average_blink_rate == 18.5
        assert sessions[0].status == "completed"

    def test_end_session_interrupted(self, repo: MonitoringRepository) -> None:
        """Should mark interrupted sessions correctly."""
        session_id = repo.create_session()
        repo.end_session(session_id, interrupted=True)
        sessions = repo.get_recent_sessions()
        assert sessions[0].status == "interrupted"
        assert sessions[0].interrupted == 1

    def test_add_measurement(self, repo: MonitoringRepository) -> None:
        """Should add a blink measurement to a session."""
        session_id = repo.create_session()
        now = datetime.utcnow()
        measurement_id = repo.add_measurement(
            session_id,
            window_start=now - timedelta(minutes=1),
            window_end=now,
            blink_count=5,
            estimated_blink_rate=15.0,
            valid_observation_seconds=60.0,
        )
        assert measurement_id is not None

        measurements = repo.get_session_measurements(session_id)
        assert len(measurements) == 1
        assert measurements[0].blink_count == 5
        assert measurements[0].estimated_blink_rate == 15.0

    def test_multiple_measurements(self, repo: MonitoringRepository) -> None:
        """Should track multiple measurements per session."""
        session_id = repo.create_session()
        now = datetime.utcnow()

        for i in range(5):
            repo.add_measurement(
                session_id,
                window_start=now - timedelta(minutes=5 - i),
                window_end=now - timedelta(minutes=4 - i),
                blink_count=i,
                estimated_blink_rate=float(i * 3),
                valid_observation_seconds=60.0,
            )

        measurements = repo.get_session_measurements(session_id)
        assert len(measurements) == 5

    def test_get_recent_sessions_order(self, repo: MonitoringRepository) -> None:
        """Sessions should be ordered by creation date descending."""
        repo.create_session()
        id2 = repo.create_session()
        sessions = repo.get_recent_sessions()
        assert len(sessions) == 2
        assert sessions[0].id == id2  # Most recent first

    def test_delete_all(self, repo: MonitoringRepository) -> None:
        """Should delete all monitoring data."""
        session_id = repo.create_session()
        repo.add_measurement(
            session_id,
            window_start=datetime.utcnow(),
            window_end=datetime.utcnow(),
            blink_count=5,
            estimated_blink_rate=15.0,
            valid_observation_seconds=60.0,
        )
        count = repo.delete_all()
        assert count >= 2  # At least session + measurement

    def test_end_nonexistent_session(self, repo: MonitoringRepository) -> None:
        """Ending a nonexistent session should not raise."""
        repo.end_session("nonexistent-id", total_blinks=5)
        # Should not raise

    def test_algorithm_version(self, repo: MonitoringRepository) -> None:
        """Measurements should track algorithm version."""
        session_id = repo.create_session()
        now = datetime.utcnow()
        repo.add_measurement(
            session_id,
            window_start=now,
            window_end=now,
            blink_count=1,
            estimated_blink_rate=12.0,
            valid_observation_seconds=60.0,
            algorithm_version="2.0",
        )
        measurements = repo.get_session_measurements(session_id)
        assert measurements[0].algorithm_version == "2.0"
