"""Animation engine — reusable animation system for exercise visualizations.

Provides a base AnimationEngine with concrete implementations for each
exercise animation type. All animations use Qt's QTimer for smooth,
deterministic playback that integrates with the exercise controller.
"""

from __future__ import annotations

import logging
import math
from enum import Enum
from typing import Protocol

from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPainterPath
from PySide6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class AnimationState(Enum):
    """State of an animation lifecycle."""

    IDLE = "idle"
    PLAYING = "playing"
    PAUSED = "paused"
    COMPLETED = "completed"


class AnimationCallbacks(Protocol):
    """Interface for animation completion callbacks."""

    def on_animation_complete(self) -> None: ...


class AnimationEngine(QWidget):
    """Base class for exercise animations.

    Renders a smooth, theme-aware visual target that follows a controlled
    path. Subclasses implement specific movement patterns.

    Signals:
        progress_updated: Emitted with 0.0-1.0 progress on each frame.
    """

    progress_updated = Signal(float)

    # Timing
    _FRAME_MS = 16  # ~60fps

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._state = AnimationState.IDLE
        self._progress = 0.0
        self._duration_ms = 0
        self._elapsed_ms = 0
        self._last_tick_ms = 0

        # Target rendering
        self._target_x = 0.5  # Normalized 0.0-1.0
        self._target_y = 0.5
        self._target_size = 16
        self._target_color = QColor("#3B82F6")
        self._trail_points: list[tuple[float, float]] = []

        # Timer
        self._timer = QTimer(self)
        self._timer.setInterval(self._FRAME_MS)
        self._timer.timeout.connect(self._tick)

        self.setMinimumHeight(200)
        self.setMinimumWidth(200)

    @property
    def state(self) -> AnimationState:
        return self._state

    @property
    def progress(self) -> float:
        return self._progress

    def start(self, duration_seconds: int) -> None:
        """Start the animation."""
        self._duration_ms = duration_seconds * 1000
        self._elapsed_ms = 0
        self._progress = 0.0
        self._trail_points.clear()
        self._state = AnimationState.PLAYING
        self._last_tick_ms = _now_ms()
        self._on_start()
        self._timer.start()
        self.update()

    def pause(self) -> None:
        """Pause the animation."""
        if self._state == AnimationState.PLAYING:
            self._state = AnimationState.PAUSED
            self._timer.stop()

    def resume(self) -> None:
        """Resume from pause."""
        if self._state == AnimationState.PAUSED:
            self._state = AnimationState.PLAYING
            self._last_tick_ms = _now_ms()
            self._timer.start()

    def reset(self) -> None:
        """Reset to idle state."""
        self._timer.stop()
        self._state = AnimationState.IDLE
        self._progress = 0.0
        self._elapsed_ms = 0
        self._trail_points.clear()
        self._on_reset()
        self.update()

    def stop(self) -> None:
        """Stop and reset."""
        self.reset()

    def cleanup(self) -> None:
        """Release resources."""
        self._timer.stop()

    def set_target_color(self, color: QColor) -> None:
        """Set the target dot color."""
        self._target_color = color

    def _tick(self) -> None:
        """Timer tick — advance animation."""
        now = _now_ms()
        dt = now - self._last_tick_ms
        self._last_tick_ms = now

        if self._state != AnimationState.PLAYING:
            return

        self._elapsed_ms += dt

        if self._duration_ms > 0:
            self._progress = min(1.0, self._elapsed_ms / self._duration_ms)
        else:
            self._progress = 1.0

        self._on_tick(self._progress, dt / 1000.0)
        self.progress_updated.emit(self._progress)
        self.update()

        if self._progress >= 1.0:
            self._state = AnimationState.COMPLETED
            self._timer.stop()
            self._on_complete()

    def _on_start(self) -> None:
        """Override in subclass for start logic."""

    def _on_reset(self) -> None:
        """Override in subclass for reset logic."""

    def _on_tick(self, progress: float, dt: float) -> None:
        """Override in subclass for per-frame logic."""

    def _on_complete(self) -> None:
        """Override in subclass for completion logic."""

    def paintEvent(self, _event: object) -> None:  # noqa: N802
        """Render the animation target."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w * self._target_x
        cy = h * self._target_y

        # Draw trail
        if self._trail_points:
            path = QPainterPath()
            first = True
            for px, py in self._trail_points:
                px_abs = w * px
                py_abs = h * py
                if first:
                    path.moveTo(px_abs, py_abs)
                    first = False
                else:
                    path.lineTo(px_abs, py_abs)
            painter.setPen(_pen_color(self._target_color, 60))
            painter.drawPath(path)

        # Draw target circle
        painter.setBrush(self._target_color)
        painter.setPen(_pen_color(self._target_color, 180))
        painter.drawEllipse(int(cx - self._target_size), int(cy - self._target_size),
                            self._target_size * 2, self._target_size * 2)

        # Draw center dot
        painter.setBrush(QColor("#FFFFFF"))
        painter.setPen(_pen_color(QColor("#FFFFFF"), 200))
        dot = max(3, self._target_size // 4)
        painter.drawEllipse(int(cx - dot), int(cy - dot), dot * 2, dot * 2)

        painter.end()


# ---------------------------------------------------------------------------
# Concrete animations
# ---------------------------------------------------------------------------


class BlinkAnimation(AnimationEngine):
    """Blink exercise — pulsing circle that simulates eye opening/closing."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._blink_phase = 0.0
        self._blink_speed = 2.5  # blinks per second

    def _on_start(self) -> None:
        self._blink_phase = 0.0

    def _on_tick(self, _progress: float, _dt: float) -> None:
        self._blink_phase += _dt * self._blink_speed
        # Smooth sine wave for open/close cycle
        eye_openness = (math.sin(self._blink_phase * math.pi * 2) + 1) / 2
        # Scale target size: open = large, closed = thin line
        self._target_size = int(8 + eye_openness * 20)
        # Keep target centered
        self._target_x = 0.5
        self._target_y = 0.5

    def _on_reset(self) -> None:
        self._blink_phase = 0.0
        self._target_size = 16


class LookAwayAnimation(AnimationEngine):
    """Look away — target moves left-to-right with gentle easing."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._sweep_speed = 0.3  # cycles per second

    def _on_tick(self, progress: float, _dt: float) -> None:
        t = progress * self._sweep_speed * 10
        # Smooth back-and-forth with ease-in-out
        raw = (math.sin(t * math.pi * 2) + 1) / 2
        eased = _ease_in_out(raw)
        self._target_x = 0.15 + eased * 0.7  # 15% to 85%
        self._target_y = 0.5
        self._target_size = 16
        self._trail_points.append((self._target_x, self._target_y))
        if len(self._trail_points) > 80:
            self._trail_points.pop(0)


class NearFarAnimation(AnimationEngine):
    """Near-far focus — target grows and shrinks to simulate depth."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._cycle_speed = 0.25  # cycles per second

    def _on_tick(self, progress: float, _dt: float) -> None:
        t = progress * self._cycle_speed * 10
        # Smooth oscillation between near (big) and far (small)
        cycle = (math.sin(t * math.pi * 2) + 1) / 2
        eased = _ease_in_out(cycle)
        # Near = large target, far = small target
        self._target_size = int(10 + eased * 26)
        self._target_x = 0.5
        self._target_y = 0.5
        self._target_color = _lerp_color(
            QColor("#3B82F6"), QColor("#8B5CF6"), eased
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _now_ms() -> int:
    """Current monotonic time in milliseconds."""
    import time
    return int(time.monotonic() * 1000)


def _ease_in_out(t: float) -> float:
    """Smooth ease-in-out."""
    return t * t * (3 - 2 * t)


def _pen_color(base: QColor, alpha: int) -> QColor:
    """Create a pen color with given alpha."""
    c = QColor(base)
    c.setAlpha(alpha)
    return c


def _lerp_color(a: QColor, b: QColor, t: float) -> QColor:
    """Linearly interpolate between two colors."""
    r = int(a.red() + (b.red() - a.red()) * t)
    g = int(a.green() + (b.green() - a.green()) * t)
    bl = int(a.blue() + (b.blue() - a.blue()) * t)
    return QColor(r, g, bl)


def create_animation(anim_type: str, parent: QWidget | None = None) -> AnimationEngine:
    """Factory: create the appropriate animation engine for a type string.

    Supported types: blink, look_away, near_far, distance_focus,
    eye_rolling, palming, figure_eight.
    """
    mapping: dict[str, type[AnimationEngine]] = {
        "blink": BlinkAnimation,
        "look_away": LookAwayAnimation,
        "near_far": NearFarAnimation,
        "distance_focus": LookAwayAnimation,
        "eye_rolling": LookAwayAnimation,
        "palming": BlinkAnimation,
        "figure_eight": LookAwayAnimation,
    }
    cls = mapping.get(anim_type, LookAwayAnimation)
    return cls(parent=parent)
