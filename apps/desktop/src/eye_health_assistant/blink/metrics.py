"""Blink metrics — rolling window aggregation and rate calculation."""

from __future__ import annotations

import logging
import time
from collections import deque
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class BlinkSample:
    """A single blink observation."""

    timestamp: float
    blink_count: int
    valid_observation_seconds: float


@dataclass
class BlinkMetrics:
    """Aggregated blink metrics over a rolling window."""

    estimated_blink_rate: float | None  # blinks per minute, None if insufficient data
    total_blinks: int
    valid_observation_seconds: float
    window_seconds: float
    has_sufficient_data: bool


class MetricsAggregator:
    """Rolling window blink rate calculator.

    Maintains a deque of blink samples and calculates the estimated
    blink rate over a configurable rolling window. Excludes periods
    with no face detected from the rate calculation.
    """

    def __init__(
        self,
        window_seconds: float = 180.0,
        min_observation_seconds: float = 30.0,
    ) -> None:
        """
        Args:
            window_seconds: Rolling window duration in seconds.
            min_observation_seconds: Minimum valid observation time before
                a blink rate is reported.
        """
        self._window_seconds = window_seconds
        self._min_observation = min_observation_seconds
        self._samples: deque[BlinkSample] = deque()
        self._total_blinks = 0
        self._total_valid_seconds = 0.0
        self._session_start: float | None = None

    def start_session(self) -> None:
        """Mark the start of a monitoring session."""
        self._session_start = time.monotonic()
        self._samples.clear()
        self._total_blinks = 0
        self._total_valid_seconds = 0.0

    def add_sample(
        self,
        blink_count: int,
        valid_observation_seconds: float,
    ) -> None:
        """Add a blink count sample to the rolling window.

        Args:
            blink_count: Number of blinks detected since last sample.
            valid_observation_seconds: Seconds of valid face-detected
                observation since last sample.
        """
        now = time.monotonic()
        sample = BlinkSample(
            timestamp=now,
            blink_count=blink_count,
            valid_observation_seconds=valid_observation_seconds,
        )
        self._samples.append(sample)
        self._total_blinks += blink_count
        self._total_valid_seconds += valid_observation_seconds

        # Evict old samples outside the rolling window
        cutoff = now - self._window_seconds
        while self._samples and self._samples[0].timestamp < cutoff:
            old = self._samples.popleft()
            self._total_blinks -= old.blink_count
            self._total_valid_seconds -= old.valid_observation_seconds

    def get_metrics(self) -> BlinkMetrics:
        """Calculate current blink metrics over the rolling window.

        Returns:
            BlinkMetrics with estimated rate or None if insufficient data.
        """
        # Ensure non-negative totals
        total_blinks = max(0, self._total_blinks)
        total_valid = max(0.0, self._total_valid_seconds)

        has_sufficient = total_valid >= self._min_observation

        if has_sufficient and total_valid > 0:
            rate = (total_blinks / total_valid) * 60.0
        else:
            rate = None

        return BlinkMetrics(
            estimated_blink_rate=rate,
            total_blinks=total_blinks,
            valid_observation_seconds=total_valid,
            window_seconds=self._window_seconds,
            has_sufficient_data=has_sufficient,
        )

    def reset(self) -> None:
        """Reset all accumulated data."""
        self._samples.clear()
        self._total_blinks = 0
        self._total_valid_seconds = 0.0
        self._session_start = None
