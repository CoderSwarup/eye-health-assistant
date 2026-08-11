"""Tests for blink metrics rolling window aggregator."""

from __future__ import annotations

import pytest

from eye_health_assistant.blink.metrics import MetricsAggregator


class TestMetricsAggregator:
    """Test rolling window blink rate calculation."""

    def setup_method(self) -> None:
        self.agg = MetricsAggregator(
            window_seconds=10.0,
            min_observation_seconds=5.0,
        )
        self.agg.start_session()

    def test_initial_state(self) -> None:
        """Fresh session should have no data."""
        metrics = self.agg.get_metrics()
        assert metrics.estimated_blink_rate is None
        assert metrics.total_blinks == 0
        assert not metrics.has_sufficient_data

    def test_insufficient_data(self) -> None:
        """Should not report rate until minimum observation time."""
        self.agg.add_sample(blink_count=5, valid_observation_seconds=3.0)
        metrics = self.agg.get_metrics()
        assert metrics.estimated_blink_rate is None
        assert not metrics.has_sufficient_data

    def test_sufficient_data(self) -> None:
        """Should report rate after minimum observation time."""
        self.agg.add_sample(blink_count=10, valid_observation_seconds=10.0)
        metrics = self.agg.get_metrics()
        assert metrics.estimated_blink_rate is not None
        assert metrics.has_sufficient_data
        assert metrics.estimated_blink_rate == pytest.approx(60.0, abs=0.1)

    def test_rate_calculation(self) -> None:
        """Blink rate should be blinks/minutes."""
        # 15 blinks in 60 seconds = 15 blinks/min
        self.agg.add_sample(blink_count=15, valid_observation_seconds=60.0)
        metrics = self.agg.get_metrics()
        assert metrics.estimated_blink_rate == pytest.approx(15.0, abs=0.1)

    def test_rolling_window(self) -> None:
        """Old samples outside the window should be excluded."""
        # Add old sample (manually backdate)
        self.agg._samples.clear()
        self.agg._total_blinks = 0
        self.agg._total_valid_seconds = 0.0

        # Add a sample that's now
        self.agg.add_sample(blink_count=10, valid_observation_seconds=10.0)

        # Simulate an old sample by manipulating timestamps
        old_sample = self.agg._samples[0]
        self.agg._samples[0] = type(old_sample)(
            timestamp=old_sample.timestamp - 15.0,  # Outside 10s window
            blink_count=5,
            valid_observation_seconds=5.0,
        )
        self.agg._total_blinks = 15  # Both samples counted
        self.agg._total_valid_seconds = 15.0

        # Add a new sample to trigger eviction
        self.agg.add_sample(blink_count=0, valid_observation_seconds=1.0)

        metrics = self.agg.get_metrics()
        # Only the second and third samples should count (10 + 0 blinks)
        assert metrics.total_blinks == 10

    def test_no_face_periods(self) -> None:
        """Zero blink counts should still track observation time."""
        self.agg.add_sample(blink_count=0, valid_observation_seconds=10.0)
        metrics = self.agg.get_metrics()
        assert metrics.has_sufficient_data
        assert metrics.estimated_blink_rate == 0.0

    def test_mixed_samples(self) -> None:
        """Multiple samples should aggregate correctly."""
        self.agg.add_sample(blink_count=5, valid_observation_seconds=10.0)
        self.agg.add_sample(blink_count=3, valid_observation_seconds=10.0)
        self.agg.add_sample(blink_count=7, valid_observation_seconds=10.0)

        metrics = self.agg.get_metrics()
        assert metrics.total_blinks == 15
        assert metrics.valid_observation_seconds == 30.0
        # 15 blinks / 30 seconds * 60 = 30 blinks/min
        assert metrics.estimated_blink_rate == pytest.approx(30.0, abs=0.1)

    def test_reset(self) -> None:
        """Reset should clear all accumulated data."""
        self.agg.add_sample(blink_count=10, valid_observation_seconds=10.0)
        self.agg.reset()
        metrics = self.agg.get_metrics()
        assert metrics.total_blinks == 0
        assert metrics.valid_observation_seconds == 0.0
        assert metrics.estimated_blink_rate is None

    def test_custom_thresholds(self) -> None:
        """Should respect custom minimum observation time."""
        agg = MetricsAggregator(
            window_seconds=60.0,
            min_observation_seconds=60.0,
        )
        agg.start_session()
        agg.add_sample(blink_count=10, valid_observation_seconds=30.0)
        metrics = agg.get_metrics()
        assert not metrics.has_sufficient_data

    def test_window_eviction(self) -> None:
        """Samples outside the window should be evicted."""
        agg = MetricsAggregator(window_seconds=5.0, min_observation_seconds=1.0)
        agg.start_session()

        # Add sample
        agg.add_sample(blink_count=10, valid_observation_seconds=5.0)

        # Manually backdate the sample
        if agg._samples:
            agg._samples[0] = type(agg._samples[0])(
                timestamp=agg._samples[0].timestamp - 10.0,
                blink_count=10,
                valid_observation_seconds=5.0,
            )

        # Add another sample to trigger eviction
        agg.add_sample(blink_count=5, valid_observation_seconds=2.0)

        metrics = agg.get_metrics()
        # Old sample should be evicted
        assert metrics.total_blinks == 5
