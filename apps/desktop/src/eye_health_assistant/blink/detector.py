"""Blink detector — state machine for detecting eye blinks."""

from __future__ import annotations

import logging
from enum import Enum, auto

logger = logging.getLogger(__name__)


class BlinkState(Enum):
    """State machine for blink detection."""

    EYES_OPEN = auto()
    EYES_CLOSING = auto()
    EYES_CLOSED = auto()


class BlinkDetector:
    """Detects blink events using a state machine with hysteresis.

    A blink is defined as a complete open -> closed -> open transition.
    The detector uses two thresholds (close and open) to avoid noise
    and duplicate counts.

    State machine:
        EYES_OPEN
            ↓ openness below close_threshold
        EYES_CLOSING
            ↓ openness below closed_threshold (sufficiently closed)
        EYES_CLOSED
            ↓ openness above open_threshold
        BLINK_DETECTED -> EYES_OPEN
    """

    def __init__(
        self,
        close_threshold: float = 0.22,
        open_threshold: float = 0.28,
        closed_threshold: float = 0.20,
    ) -> None:
        """
        Args:
            close_threshold: EAR value below which eyes start closing.
            open_threshold: EAR value above which eyes are considered open again.
            closed_threshold: EAR value below which eyes are fully closed.
        """
        self._close_threshold = close_threshold
        self._open_threshold = open_threshold
        self._closed_threshold = closed_threshold
        self._state = BlinkState.EYES_OPEN
        self._closed_frames = 0

    @property
    def state(self) -> BlinkState:
        return self._state

    @property
    def is_open(self) -> bool:
        return self._state == BlinkState.EYES_OPEN

    def process(self, openness: float | None) -> bool:
        """Process an eye openness value and return whether a blink occurred.

        Args:
            openness: The current EAR value, or None if no face detected.

        Returns:
            True if a complete blink was detected on this frame.
        """
        if openness is None:
            # No face — reset to open state
            if self._state != BlinkState.EYES_OPEN:
                logger.debug("No face detected, resetting blink state")
            self._state = BlinkState.EYES_OPEN
            self._closed_frames = 0
            return False

        blink_detected = False

        if self._state == BlinkState.EYES_OPEN:
            if openness < self._close_threshold:
                self._state = BlinkState.EYES_CLOSING
                self._closed_frames = 0
                logger.debug("Eyes closing: EAR=%.3f", openness)

        elif self._state == BlinkState.EYES_CLOSING:
            if openness < self._closed_threshold:
                self._state = BlinkState.EYES_CLOSED
                self._closed_frames = 1
                logger.debug("Eyes closed: EAR=%.3f", openness)
            elif openness >= self._open_threshold:
                # Reopened before fully closing — false alarm
                self._state = BlinkState.EYES_OPEN
                self._closed_frames = 0

        elif self._state == BlinkState.EYES_CLOSED:
            if openness >= self._open_threshold:
                # Complete blink!
                blink_detected = True
                self._state = BlinkState.EYES_OPEN
                self._closed_frames = 0
                logger.debug("Blink detected: EAR=%.3f", openness)
            else:
                self._closed_frames += 1

        return blink_detected

    def reset(self) -> None:
        """Reset the detector to initial state."""
        self._state = BlinkState.EYES_OPEN
        self._closed_frames = 0
