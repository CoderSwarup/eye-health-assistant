"""Analytics service — aggregates data from repositories into analytics models."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from eye_health_assistant.infrastructure.database.engine import Database
from eye_health_assistant.infrastructure.database.models import (
    BlinkMeasurementRow,
    MonitoringSessionRow,
    TimerSessionRow,
)

logger = logging.getLogger(__name__)


class TimePeriod(Enum):
    """Analytics time period."""

    TODAY = "today"
    WEEK = "week"
    MONTH = "month"
    ALL = "all"


@dataclass
class DailyAggregates:
    """Aggregated data for a single day."""

    date: datetime
    focus_seconds: float = 0.0
    break_seconds: float = 0.0
    focus_sessions_completed: int = 0
    monitoring_seconds: float = 0.0
    total_blinks: int = 0
    blink_rate_samples: list[float] = field(default_factory=list)
    exercises_completed: int = 0

    @property
    def avg_blink_rate(self) -> float | None:
        if not self.blink_rate_samples:
            return None
        return sum(self.blink_rate_samples) / len(self.blink_rate_samples)

    @property
    def total_activity_seconds(self) -> float:
        return self.focus_seconds + self.break_seconds + self.monitoring_seconds


@dataclass
class PeriodSummary:
    """Summary analytics for a time period."""

    period: TimePeriod
    start_date: datetime
    end_date: datetime

    total_focus_seconds: float = 0.0
    total_break_seconds: float = 0.0
    total_monitoring_seconds: float = 0.0
    focus_sessions_completed: int = 0
    total_blinks: int = 0
    total_blink_observation_seconds: float = 0.0
    monitoring_sessions_count: int = 0
    exercises_completed: int = 0
    active_days: int = 0

    daily_data: list[DailyAggregates] = field(default_factory=list)

    @property
    def total_focus_hours(self) -> float:
        return self.total_focus_seconds / 3600.0

    @property
    def total_break_hours(self) -> float:
        return self.total_break_seconds / 3600.0

    @property
    def total_monitoring_hours(self) -> float:
        return self.total_monitoring_seconds / 3600.0

    @property
    def avg_daily_focus_hours(self) -> float:
        if self.active_days == 0:
            return 0.0
        return self.total_focus_hours / self.active_days

    @property
    def avg_blink_rate(self) -> float | None:
        if self.total_blink_observation_seconds <= 0:
            return None
        return self.total_blinks / (self.total_blink_observation_seconds / 60.0)

    @property
    def focus_hours_display(self) -> str:
        h = int(self.total_focus_seconds // 3600)
        m = int((self.total_focus_seconds % 3600) // 60)
        if h > 0:
            return f"{h}h {m}m"
        return f"{m}m"

    @property
    def break_hours_display(self) -> str:
        h = int(self.total_break_seconds // 3600)
        m = int((self.total_break_seconds % 3600) // 60)
        if h > 0:
            return f"{h}h {m}m"
        return f"{m}m"

    @property
    def monitoring_hours_display(self) -> str:
        h = int(self.total_monitoring_seconds // 3600)
        m = int((self.total_monitoring_seconds % 3600) // 60)
        if h > 0:
            return f"{h}h {m}m"
        return f"{m}m"

    @property
    def blink_rate_display(self) -> str:
        rate = self.avg_blink_rate
        if rate is None:
            return "--"
        return f"{rate:.1f}/min"


@dataclass
class ComparisonResult:
    """Comparison between two periods."""

    current: PeriodSummary
    previous: PeriodSummary

    @property
    def focus_change_pct(self) -> float | None:
        if self.previous.total_focus_seconds == 0:
            return None
        return (
            (self.current.total_focus_seconds - self.previous.total_focus_seconds)
            / self.previous.total_focus_seconds
        ) * 100

    @property
    def break_change_pct(self) -> float | None:
        if self.previous.total_break_seconds == 0:
            return None
        return (
            (self.current.total_break_seconds - self.previous.total_break_seconds)
            / self.previous.total_break_seconds
        ) * 100

    @property
    def blink_rate_change(self) -> float | None:
        prev_rate = self.previous.avg_blink_rate
        curr_rate = self.current.avg_blink_rate
        if prev_rate is None or curr_rate is None:
            return None
        return curr_rate - prev_rate


class AnalyticsService:
    """Service for computing analytics from raw session data."""

    def __init__(self, database: Database) -> None:
        self._db = database

    def get_summary(self, period: TimePeriod) -> PeriodSummary:
        """Get aggregated summary for a time period."""
        start, end = self._get_period_range(period)
        daily = self._aggregate_daily(start, end)
        return self._summarize_daily(period, start, end, daily)

    def get_comparison(self, period: TimePeriod) -> ComparisonResult | None:
        """Compare current period with previous period."""
        start, end = self._get_period_range(period)
        prev_start, prev_end = self._get_previous_period_range(period)

        current_daily = self._aggregate_daily(start, end)
        previous_daily = self._aggregate_daily(prev_start, prev_end)

        current = self._summarize_daily(period, start, end, current_daily)
        previous = self._summarize_daily(period, prev_start, prev_end, previous_daily)

        return ComparisonResult(current=current, previous=previous)

    def get_daily_trend(self, period: TimePeriod) -> list[DailyAggregates]:
        """Get daily data for trend visualization."""
        start, end = self._get_period_range(period)
        return self._aggregate_daily(start, end)

    def get_today_summary(self) -> PeriodSummary:
        """Get today's summary."""
        return self.get_summary(TimePeriod.TODAY)

    def _get_period_range(self, period: TimePeriod) -> tuple[datetime, datetime]:
        """Get start and end datetime for a period."""
        now = datetime.utcnow()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        if period == TimePeriod.TODAY:
            return today, now
        elif period == TimePeriod.WEEK:
            start = today - timedelta(days=today.weekday())
            return start, now
        elif period == TimePeriod.MONTH:
            start = today.replace(day=1)
            return start, now
        else:
            return datetime.min, now

    def _get_previous_period_range(
        self, period: TimePeriod
    ) -> tuple[datetime, datetime]:
        """Get the period range immediately before the current period."""
        start, end = self._get_period_range(period)
        duration = end - start
        prev_end = start
        prev_start = prev_end - duration
        return prev_start, prev_end

    def _aggregate_daily(
        self, start: datetime, end: datetime
    ) -> list[DailyAggregates]:
        """Aggregate raw data into daily buckets."""
        daily_map: dict[str, DailyAggregates] = {}

        with self._db.get_session() as db_session:
            # Timer sessions
            timer_rows = (
                db_session.query(TimerSessionRow)
                .filter(
                    TimerSessionRow.started_at.isnot(None),
                    TimerSessionRow.started_at >= start,
                    TimerSessionRow.started_at <= end,
                )
                .all()
            )

            for row in timer_rows:
                if row.started_at is None:
                    continue
                day_key = row.started_at.strftime("%Y-%m-%d")
                if day_key not in daily_map:
                    daily_map[day_key] = DailyAggregates(
                        date=row.started_at.replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                    )
                daily = daily_map[day_key]
                daily.focus_seconds += float(row.total_focus_seconds or 0)
                daily.break_seconds += float(row.total_break_seconds or 0)
                daily.focus_sessions_completed += int(row.completed_focus_sessions or 0)

            # Monitoring sessions
            monitoring_rows = (
                db_session.query(MonitoringSessionRow)
                .filter(
                    MonitoringSessionRow.started_at.isnot(None),
                    MonitoringSessionRow.started_at >= start,
                    MonitoringSessionRow.started_at <= end,
                )
                .all()
            )

            for mon_row in monitoring_rows:
                if mon_row.started_at is None:
                    continue
                day_key = mon_row.started_at.strftime("%Y-%m-%d")
                if day_key not in daily_map:
                    daily_map[day_key] = DailyAggregates(
                        date=mon_row.started_at.replace(
                            hour=0, minute=0, second=0, microsecond=0
                        )
                    )
                daily = daily_map[day_key]
                daily.monitoring_seconds += float(mon_row.duration_seconds or 0)
                daily.total_blinks += int(mon_row.total_blinks or 0)
                if (
                    mon_row.average_blink_rate is not None
                    and mon_row.valid_observation_seconds is not None
                    and float(mon_row.valid_observation_seconds) > 0
                ):
                    daily.blink_rate_samples.append(
                        float(mon_row.average_blink_rate)
                    )

        # Sort by date
        return sorted(daily_map.values(), key=lambda d: d.date)

    def _summarize_daily(
        self,
        period: TimePeriod,
        start: datetime,
        end: datetime,
        daily: list[DailyAggregates],
    ) -> PeriodSummary:
        """Create a PeriodSummary from daily aggregates."""
        summary = PeriodSummary(
            period=period,
            start_date=start,
            end_date=end,
            daily_data=daily,
        )

        for d in daily:
            summary.total_focus_seconds += d.focus_seconds
            summary.total_break_seconds += d.break_seconds
            summary.total_monitoring_seconds += d.monitoring_seconds
            summary.focus_sessions_completed += d.focus_sessions_completed
            summary.total_blinks += d.total_blinks
            summary.exercises_completed += d.exercises_completed
            if d.total_activity_seconds > 0:
                summary.active_days += 1

        # Calculate blink observation seconds from daily samples
        # Each sample represents an observation window
        # We use the number of samples * average window length
        total_samples = sum(len(d.blink_rate_samples) for d in daily)
        if total_samples > 0:
            summary.monitoring_sessions_count = total_samples
            # Estimate observation seconds from daily data
            # Each blink rate sample represents roughly 5 minutes of observation
            summary.total_blink_observation_seconds = total_samples * 300.0

        return summary

    def delete_all_data(self) -> int:
        """Delete all analytics data. Returns count of records deleted."""
        count = 0
        with self._db.get_session() as db_session:
            count += db_session.query(BlinkMeasurementRow).delete()
            count += db_session.query(MonitoringSessionRow).delete()
            count += db_session.query(TimerSessionRow).delete()
            db_session.commit()
        return count

    def delete_timer_sessions(self) -> int:
        """Delete all timer sessions."""
        with self._db.get_session() as db_session:
            count = db_session.query(TimerSessionRow).delete()
            db_session.commit()
            return count

    def delete_monitoring_sessions(self) -> int:
        """Delete all monitoring sessions and blink measurements."""
        with self._db.get_session() as db_session:
            count = db_session.query(BlinkMeasurementRow).delete()
            count += db_session.query(MonitoringSessionRow).delete()
            db_session.commit()
            return count

    def export_all_data(self) -> dict:
        """Export all data as a dictionary for JSON/CSV serialization."""
        data: dict = {
            "exported_at": datetime.utcnow().isoformat(),
            "timer_sessions": [],
            "monitoring_sessions": [],
            "blink_measurements": [],
        }

        with self._db.get_session() as db_session:
            # Timer sessions
            timer_rows = db_session.query(TimerSessionRow).all()
            for row in timer_rows:
                started = row.started_at.isoformat() if row.started_at else None
                ended = row.ended_at.isoformat() if row.ended_at else None
                created = row.created_at.isoformat() if row.created_at else None
                data["timer_sessions"].append(
                    {
                        "id": row.id,
                        "mode": row.mode,
                        "status": row.status,
                        "phase": row.phase,
                        "focus_duration": row.focus_duration,
                        "break_duration": row.break_duration,
                        "started_at": started,
                        "ended_at": ended,
                        "total_focus_seconds": row.total_focus_seconds,
                        "total_break_seconds": row.total_break_seconds,
                        "completed_focus_sessions": row.completed_focus_sessions,
                        "interrupted": bool(row.interrupted),
                        "created_at": created,
                    }
                )

            # Monitoring sessions
            monitoring_rows = db_session.query(MonitoringSessionRow).all()
            for mon_row in monitoring_rows:
                started = (
                    mon_row.started_at.isoformat() if mon_row.started_at else None
                )
                ended = mon_row.ended_at.isoformat() if mon_row.ended_at else None
                created = (
                    mon_row.created_at.isoformat() if mon_row.created_at else None
                )
                data["monitoring_sessions"].append(
                    {
                        "id": mon_row.id,
                        "status": mon_row.status,
                        "device_index": mon_row.device_index,
                        "started_at": started,
                        "ended_at": ended,
                        "duration_seconds": mon_row.duration_seconds,
                        "total_blinks": mon_row.total_blinks,
                        "average_blink_rate": mon_row.average_blink_rate,
                        "valid_observation_seconds": mon_row.valid_observation_seconds,
                        "reminders_sent": mon_row.reminders_sent,
                        "interrupted": bool(mon_row.interrupted),
                        "created_at": created,
                    }
                )

            # Blink measurements
            blink_rows = db_session.query(BlinkMeasurementRow).all()
            for blink_row in blink_rows:
                win_start = (
                    blink_row.window_start.isoformat()
                    if blink_row.window_start
                    else None
                )
                win_end = (
                    blink_row.window_end.isoformat()
                    if blink_row.window_end
                    else None
                )
                created = (
                    blink_row.created_at.isoformat()
                    if blink_row.created_at
                    else None
                )
                data["blink_measurements"].append(
                    {
                        "id": blink_row.id,
                        "session_id": blink_row.session_id,
                        "window_start": win_start,
                        "window_end": win_end,
                        "blink_count": blink_row.blink_count,
                        "estimated_blink_rate": blink_row.estimated_blink_rate,
                        "valid_observation_seconds": (
                            blink_row.valid_observation_seconds
                        ),
                        "algorithm_version": blink_row.algorithm_version,
                        "created_at": created,
                    }
                )

        return data
