"""Tests for analytics service — aggregation, export, and deletion."""

from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from eye_health_assistant.analytics.service import (
    AnalyticsService,
    ComparisonResult,
    DailyAggregates,
    PeriodSummary,
    TimePeriod,
)
from eye_health_assistant.infrastructure.database.engine import Database
from eye_health_assistant.infrastructure.database.models import (
    Base,
    BlinkMeasurementRow,
    MonitoringSessionRow,
    TimerSessionRow,
)


@pytest.fixture
def in_memory_db() -> Database:
    """Create an in-memory SQLite database for testing."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    db = MagicMock(spec=Database)
    session_factory = sessionmaker(bind=engine)

    class ContextManager:
        def __init__(self) -> None:
            self.session = session_factory()

        def __enter__(self):
            return self.session

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
            self.session.close()
            return False

    db.get_session.return_value = ContextManager()
    return db


@pytest.fixture
def service(in_memory_db: Database) -> AnalyticsService:
    """Create an AnalyticsService with in-memory database."""
    return AnalyticsService(in_memory_db)


@pytest.fixture
def populated_service(in_memory_db: Database) -> AnalyticsService:
    """Create an AnalyticsService with test data populated."""
    service = AnalyticsService(in_memory_db)

    now = datetime.utcnow()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    # Add timer sessions
    with in_memory_db.get_session() as session:
        # Today's completed session
        session.add(
            TimerSessionRow(
                id="timer-1",
                mode="timer",
                status="completed",
                phase="focus",
                focus_duration=1200,
                break_duration=20,
                started_at=today + timedelta(hours=10),
                ended_at=today + timedelta(hours=10, minutes=20),
                total_focus_seconds=1200,
                total_break_seconds=20,
                completed_focus_sessions=1,
                interrupted=0,
            )
        )

        # Yesterday's session
        session.add(
            TimerSessionRow(
                id="timer-2",
                mode="timer",
                status="completed",
                phase="focus",
                focus_duration=1800,
                break_duration=30,
                started_at=yesterday + timedelta(hours=14),
                ended_at=yesterday + timedelta(hours=14, minutes=30),
                total_focus_seconds=1800,
                total_break_seconds=30,
                completed_focus_sessions=2,
                interrupted=0,
            )
        )

        # Add monitoring sessions
        session.add(
            MonitoringSessionRow(
                id="monitor-1",
                mode="smart",
                status="completed",
                device_index=0,
                started_at=today + timedelta(hours=11),
                ended_at=today + timedelta(hours=11, minutes=15),
                duration_seconds=900,
                total_blinks=150,
                average_blink_rate=15.0,
                valid_observation_seconds=600,
                reminders_sent=2,
                interrupted=0,
            )
        )

        session.add(
            MonitoringSessionRow(
                id="monitor-2",
                mode="smart",
                status="completed",
                device_index=0,
                started_at=yesterday + timedelta(hours=15),
                ended_at=yesterday + timedelta(hours=15, minutes=10),
                duration_seconds=600,
                total_blinks=90,
                average_blink_rate=18.0,
                valid_observation_seconds=400,
                reminders_sent=1,
                interrupted=0,
            )
        )

        # Add blink measurements
        session.add(
            BlinkMeasurementRow(
                id="blink-1",
                session_id="monitor-1",
                window_start=today + timedelta(hours=11),
                window_end=today + timedelta(hours=11, minutes=5),
                blink_count=50,
                estimated_blink_rate=15.0,
                valid_observation_seconds=300,
                algorithm_version="1.0",
            )
        )

        session.add(
            BlinkMeasurementRow(
                id="blink-2",
                session_id="monitor-2",
                window_start=yesterday + timedelta(hours=15),
                window_end=yesterday + timedelta(hours=15, minutes=5),
                blink_count=45,
                estimated_blink_rate=18.0,
                valid_observation_seconds=200,
                algorithm_version="1.0",
            )
        )

    return service


class TestTimePeriod:
    """Test TimePeriod enum."""

    def test_all_periods_exist(self) -> None:
        periods = [
            TimePeriod.TODAY,
            TimePeriod.WEEK,
            TimePeriod.MONTH,
            TimePeriod.ALL,
        ]
        assert len(periods) == 4

    def test_period_values(self) -> None:
        assert TimePeriod.TODAY.value == "today"
        assert TimePeriod.WEEK.value == "week"
        assert TimePeriod.MONTH.value == "month"
        assert TimePeriod.ALL.value == "all"


class TestDailyAggregates:
    """Test DailyAggregates dataclass."""

    def test_empty_day(self) -> None:
        day = DailyAggregates(date=datetime.utcnow())
        assert day.focus_seconds == 0.0
        assert day.avg_blink_rate is None
        assert day.total_activity_seconds == 0.0

    def test_blink_rate_calculation(self) -> None:
        day = DailyAggregates(
            date=datetime.utcnow(),
            blink_rate_samples=[15.0, 18.0, 20.0],
        )
        assert day.avg_blink_rate is not None
        assert abs(day.avg_blink_rate - 17.666) < 0.01

    def test_total_activity(self) -> None:
        day = DailyAggregates(
            date=datetime.utcnow(),
            focus_seconds=600,
            break_seconds=60,
            monitoring_seconds=300,
        )
        assert day.total_activity_seconds == 960.0


class TestPeriodSummary:
    """Test PeriodSummary dataclass."""

    def test_empty_summary(self) -> None:
        summary = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
        )
        assert summary.total_focus_hours == 0.0
        assert summary.avg_blink_rate is None
        assert summary.focus_hours_display == "0m"

    def test_focus_hours_display(self) -> None:
        summary = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            total_focus_seconds=3600,
        )
        assert summary.focus_hours_display == "1h 0m"

    def test_minutes_only_display(self) -> None:
        summary = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            total_focus_seconds=1200,
        )
        assert summary.focus_hours_display == "20m"

    def test_blink_rate_display(self) -> None:
        summary = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            total_blinks=150,
            total_blink_observation_seconds=600.0,  # 10 minutes of observation
        )
        assert summary.blink_rate_display == "15.0/min"

    def test_blink_rate_no_data(self) -> None:
        summary = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
        )
        assert summary.blink_rate_display == "--"


class TestComparisonResult:
    """Test ComparisonResult dataclass."""

    def test_focus_change_percentage(self) -> None:
        current = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            total_focus_seconds=120,
        )
        previous = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            total_focus_seconds=100,
        )
        comparison = ComparisonResult(current=current, previous=previous)
        assert comparison.focus_change_pct is not None
        assert abs(comparison.focus_change_pct - 20.0) < 0.01

    def test_no_previous_data(self) -> None:
        current = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            total_focus_seconds=100,
        )
        previous = PeriodSummary(
            period=TimePeriod.WEEK,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow(),
            total_focus_seconds=0,
        )
        comparison = ComparisonResult(current=current, previous=previous)
        assert comparison.focus_change_pct is None


class TestAnalyticsService:
    """Test AnalyticsService aggregation logic."""

    def test_get_summary_today(self, populated_service: AnalyticsService) -> None:
        summary = populated_service.get_summary(TimePeriod.TODAY)
        assert summary.period == TimePeriod.TODAY
        assert summary.total_focus_seconds > 0
        assert summary.focus_sessions_completed >= 1
        assert summary.monitoring_sessions_count >= 1

    def test_get_summary_week(self, populated_service: AnalyticsService) -> None:
        summary = populated_service.get_summary(TimePeriod.WEEK)
        assert summary.period == TimePeriod.WEEK
        assert summary.total_focus_seconds > 0
        assert summary.active_days >= 1

    def test_get_summary_month(self, populated_service: AnalyticsService) -> None:
        summary = populated_service.get_summary(TimePeriod.MONTH)
        assert summary.period == TimePeriod.MONTH

    def test_get_comparison(self, populated_service: AnalyticsService) -> None:
        comparison = populated_service.get_comparison(TimePeriod.WEEK)
        assert comparison is not None
        assert isinstance(comparison.current, PeriodSummary)
        assert isinstance(comparison.previous, PeriodSummary)

    def test_get_daily_trend(self, populated_service: AnalyticsService) -> None:
        daily = populated_service.get_daily_trend(TimePeriod.WEEK)
        assert isinstance(daily, list)
        assert len(daily) >= 1

    def test_empty_database(self, service: AnalyticsService) -> None:
        summary = service.get_summary(TimePeriod.WEEK)
        assert summary.total_focus_seconds == 0
        assert summary.total_blinks == 0
        assert summary.active_days == 0


class TestAnalyticsExport:
    """Test data export functionality."""

    def test_export_returns_dict(self, populated_service: AnalyticsService) -> None:
        data = populated_service.export_all_data()
        assert isinstance(data, dict)
        assert "exported_at" in data
        assert "timer_sessions" in data
        assert "monitoring_sessions" in data
        assert "blink_measurements" in data

    def test_export_contains_sessions(
        self, populated_service: AnalyticsService
    ) -> None:
        data = populated_service.export_all_data()
        assert len(data["timer_sessions"]) == 2
        assert len(data["monitoring_sessions"]) == 2
        assert len(data["blink_measurements"]) == 2

    def test_export_session_fields(
        self, populated_service: AnalyticsService
    ) -> None:
        data = populated_service.export_all_data()
        timer = data["timer_sessions"][0]
        assert "id" in timer
        assert "mode" in timer
        assert "status" in timer
        assert "started_at" in timer
        assert "total_focus_seconds" in timer

    def test_export_empty_database(self, service: AnalyticsService) -> None:
        data = service.export_all_data()
        assert data["timer_sessions"] == []
        assert data["monitoring_sessions"] == []
        assert data["blink_measurements"] == []


class TestAnalyticsDeletion:
    """Test data deletion functionality."""

    def test_delete_all_data(self, populated_service: AnalyticsService) -> None:
        count = populated_service.delete_all_data()
        assert count == 6  # 2 timer + 2 monitoring + 2 blink

        # Verify empty
        summary = populated_service.get_summary(TimePeriod.MONTH)
        assert summary.total_focus_seconds == 0

    def test_delete_timer_sessions(self, populated_service: AnalyticsService) -> None:
        count = populated_service.delete_timer_sessions()
        assert count == 2

    def test_delete_monitoring_sessions(
        self, populated_service: AnalyticsService
    ) -> None:
        count = populated_service.delete_monitoring_sessions()
        assert count == 4  # 2 monitoring + 2 blink measurements


class TestAnalyticsEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_day_range(self, service: AnalyticsService) -> None:
        summary = service.get_summary(TimePeriod.TODAY)
        assert summary.start_date <= summary.end_date

    def test_week_range(self, service: AnalyticsService) -> None:
        summary = service.get_summary(TimePeriod.WEEK)
        delta = summary.end_date - summary.start_date
        assert delta.days >= 0

    def test_month_range(self, service: AnalyticsService) -> None:
        summary = service.get_summary(TimePeriod.MONTH)
        delta = summary.end_date - summary.start_date
        assert delta.days >= 0

    def test_all_time_range(self, service: AnalyticsService) -> None:
        summary = service.get_summary(TimePeriod.ALL)
        assert summary.start_date == datetime.min

    def test_daily_data_sorted(self, populated_service: AnalyticsService) -> None:
        daily = populated_service.get_daily_trend(TimePeriod.WEEK)
        dates = [d.date for d in daily]
        assert dates == sorted(dates)
