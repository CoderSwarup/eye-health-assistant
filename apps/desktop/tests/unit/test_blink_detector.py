"""Tests for blink detector state machine."""

from __future__ import annotations

from eye_health_assistant.blink.detector import BlinkDetector, BlinkState


class TestBlinkDetector:
    """Test blink detection state machine."""

    def setup_method(self) -> None:
        self.detector = BlinkDetector(
            close_threshold=0.22,
            open_threshold=0.28,
            closed_threshold=0.20,
        )

    def test_initial_state(self) -> None:
        """Detector starts in EYES_OPEN state."""
        assert self.detector.state == BlinkState.EYES_OPEN
        assert self.detector.is_open

    def test_no_face_resets_state(self) -> None:
        """None openness resets to EYES_OPEN."""
        self.detector.process(0.15)  # Start closing
        assert self.detector.state == BlinkState.EYES_CLOSING

        blink = self.detector.process(None)
        assert not blink
        assert self.detector.state == BlinkState.EYES_OPEN

    def test_open_eyes_no_blink(self) -> None:
        """Steady open eyes should not produce blinks."""
        for _ in range(10):
            blink = self.detector.process(0.35)
            assert not blink
        assert self.detector.state == BlinkState.EYES_OPEN

    def test_simple_blink(self) -> None:
        """A complete open -> closed -> open should detect one blink."""
        # Eyes open
        self.detector.process(0.35)
        assert self.detector.state == BlinkState.EYES_OPEN

        # Eyes closing
        blink = self.detector.process(0.21)
        assert not blink
        assert self.detector.state == BlinkState.EYES_CLOSING

        # Eyes closed
        blink = self.detector.process(0.18)
        assert not blink
        assert self.detector.state == BlinkState.EYES_CLOSED

        # Eyes reopening
        blink = self.detector.process(0.30)
        assert blink
        assert self.detector.state == BlinkState.EYES_OPEN

    def test_double_blink(self) -> None:
        """Two consecutive blinks should each be detected."""
        blinks = 0

        for ear in [0.35, 0.21, 0.18, 0.30, 0.35, 0.21, 0.18, 0.30]:
            if self.detector.process(ear):
                blinks += 1

        assert blinks == 2

    def test_false_alarm_recovery(self) -> None:
        """Closing then reopening without fully closing should not count."""
        self.detector.process(0.35)  # open
        self.detector.process(0.21)  # closing
        blink = self.detector.process(0.30)  # reopened before fully closed
        assert not blink
        assert self.detector.state == BlinkState.EYES_OPEN

    def test_noise_resistance(self) -> None:
        """Brief noise spikes should not cause false blinks."""
        # Open with noise
        self.detector.process(0.35)
        self.detector.process(0.21)  # dip but not closed
        self.detector.process(0.35)  # back to open
        blink = self.detector.process(0.35)
        assert not blink

    def test_multiple_closed_frames(self) -> None:
        """Staying closed for multiple frames should only count one blink."""
        self.detector.process(0.35)  # open
        self.detector.process(0.21)  # closing
        self.detector.process(0.18)  # closed
        self.detector.process(0.18)  # still closed
        self.detector.process(0.18)  # still closed
        blink = self.detector.process(0.30)  # reopen
        assert blink

        # Second frame after reopen should not be a blink
        blink = self.detector.process(0.35)
        assert not blink

    def test_reset(self) -> None:
        """Reset should return to initial state."""
        self.detector.process(0.21)
        self.detector.process(0.18)
        self.detector.reset()
        assert self.detector.state == BlinkState.EYES_OPEN
        assert self.detector.is_open

    def test_custom_thresholds(self) -> None:
        """Detector should respect custom thresholds."""
        detector = BlinkDetector(
            close_threshold=0.25,
            open_threshold=0.30,
            closed_threshold=0.23,
        )
        # 0.24 is below close_threshold (0.25)
        detector.process(0.35)
        detector.process(0.24)
        assert detector.state == BlinkState.EYES_CLOSING

    def test_very_low_ear(self) -> None:
        """Very low EAR should go through closing to closed."""
        self.detector.process(0.35)  # open
        self.detector.process(0.10)  # Well below close_threshold -> CLOSING
        assert self.detector.state == BlinkState.EYES_CLOSING
        self.detector.process(0.10)  # Still below closed_threshold -> CLOSED
        assert self.detector.state == BlinkState.EYES_CLOSED
