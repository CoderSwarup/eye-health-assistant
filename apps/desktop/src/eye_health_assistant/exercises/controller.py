"""Exercise controller — state machine for exercise playback.

Orchestrates exercise timing, step sequencing, countdown, pause/resume,
and completion. The controller is the authoritative source of exercise
progress — the animation engine and UI both follow its state.
"""

from __future__ import annotations

import logging
import time
from enum import Enum, auto

from PySide6.QtCore import QObject, QTimer, Signal

from eye_health_assistant.domain.models.exercise import Exercise, ExerciseStep

logger = logging.getLogger(__name__)


class ExerciseState(Enum):
    """Exercise lifecycle states."""

    READY = auto()
    COUNTDOWN = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    CANCELLED = auto()


class ExerciseController(QObject):
    """Controls exercise playback with a deterministic state machine.

    Signals:
        state_changed: Emitted when the exercise state changes.
        progress_updated: Emitted with (overall_progress, step_progress).
        step_changed: Emitted with the current step index.
        countdown_tick: Emitted with remaining countdown seconds.
        completed: Emitted when the exercise finishes naturally.
    """

    state_changed = Signal(object)
    progress_updated = Signal(float, float)  # overall, step
    step_changed = Signal(int)
    countdown_tick = Signal(int)
    completed = Signal()

    _TICK_MS = 100  # 10fps timer for smooth progress

    def __init__(self, exercise: Exercise, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._exercise = exercise
        self._state = ExerciseState.READY
        self._countdown_remaining = 3

        # Timing
        self._start_time: float | None = None
        self._elapsed_at_pause: float = 0.0
        self._paused_at: float | None = None
        self._step_start_time: float | None = None
        self._step_elapsed_at_pause: float = 0.0

        # Step tracking
        self._current_step_index = 0
        self._step_start_offsets: list[float] = []
        self._compute_step_offsets()

        # Timer
        self._timer = QTimer(self)
        self._timer.setInterval(self._TICK_MS)
        self._timer.timeout.connect(self._tick)

        # Countdown timer
        self._countdown_timer = QTimer(self)
        self._countdown_timer.setInterval(1000)
        self._countdown_timer.timeout.connect(self._countdown_tick_handler)

    @property
    def state(self) -> ExerciseState:
        return self._state

    @property
    def exercise(self) -> Exercise:
        return self._exercise

    @property
    def current_step(self) -> ExerciseStep | None:
        if self._state not in (ExerciseState.RUNNING, ExerciseState.PAUSED):
            return None
        steps = self._exercise.steps
        if 0 <= self._current_step_index < len(steps):
            return steps[self._current_step_index]
        return None

    @property
    def current_step_index(self) -> int:
        return self._current_step_index

    @property
    def total_steps(self) -> int:
        return len(self._exercise.steps)

    @property
    def overall_progress(self) -> float:
        """Overall exercise progress 0.0-1.0."""
        if self._start_time is None:
            return 0.0
        elapsed = self._get_elapsed()
        return min(1.0, elapsed / self._exercise.duration_seconds)

    @property
    def step_progress(self) -> float | None:
        """Current step progress 0.0-1.0."""
        step = self.current_step
        if step is None or self._step_start_time is None:
            return None
        now = time.monotonic()
        elapsed = now - self._step_start_time
        if self._paused_at is not None and self._state == ExerciseState.PAUSED:
            elapsed = self._step_elapsed_at_pause
        if step.duration_seconds > 0:
            return min(1.0, elapsed / step.duration_seconds)
        return 1.0

    @property
    def remaining_seconds(self) -> float:
        """Seconds remaining in the exercise."""
        elapsed = self._get_elapsed()
        return max(0.0, self._exercise.duration_seconds - elapsed)

    def start(self) -> None:
        """Start the exercise with a countdown."""
        if self._state not in (ExerciseState.READY, ExerciseState.CANCELLED):
            return
        self._state = ExerciseState.COUNTDOWN
        self._countdown_remaining = 3
        self.state_changed.emit(self._state)
        self.countdown_tick.emit(self._countdown_remaining)
        self._countdown_timer.start()

    def pause(self) -> None:
        """Pause the exercise."""
        if self._state != ExerciseState.RUNNING:
            return
        self._paused_at = time.monotonic()
        self._step_elapsed_at_pause = self._get_step_elapsed()
        self._timer.stop()
        self._state = ExerciseState.PAUSED
        self.state_changed.emit(self._state)

    def resume(self) -> None:
        """Resume from pause."""
        if self._state != ExerciseState.PAUSED:
            return
        now = time.monotonic()
        if self._paused_at is not None:
            pause_duration = now - self._paused_at
            if self._start_time is not None:
                self._start_time += pause_duration
            if self._step_start_time is not None:
                self._step_start_time += pause_duration
        self._paused_at = None
        self._state = ExerciseState.RUNNING
        self._timer.start()
        self.state_changed.emit(self._state)

    def cancel(self) -> None:
        """Cancel the exercise."""
        self._timer.stop()
        self._countdown_timer.stop()
        self._state = ExerciseState.CANCELLED
        self.state_changed.emit(self._state)

    def reset(self) -> None:
        """Reset to ready state."""
        self._timer.stop()
        self._countdown_timer.stop()
        self._state = ExerciseState.READY
        self._start_time = None
        self._paused_at = None
        self._elapsed_at_pause = 0.0
        self._current_step_index = 0
        self._step_start_time = None
        self._step_elapsed_at_pause = 0.0
        self.state_changed.emit(self._state)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _compute_step_offsets(self) -> None:
        """Pre-compute cumulative start times for each step."""
        self._step_start_offsets = []
        offset = 0.0
        for step in self._exercise.steps:
            self._step_start_offsets.append(offset)
            offset += step.duration_seconds

    def _countdown_tick_handler(self) -> None:
        """Handle countdown timer tick."""
        self._countdown_remaining -= 1
        if self._countdown_remaining <= 0:
            self._countdown_timer.stop()
            self._begin_exercise()
        else:
            self.countdown_tick.emit(self._countdown_remaining)

    def _begin_exercise(self) -> None:
        """Transition from countdown to running."""
        self._start_time = time.monotonic()
        self._elapsed_at_pause = 0.0
        self._current_step_index = 0
        self._step_start_time = time.monotonic()
        self._step_elapsed_at_pause = 0.0
        self._state = ExerciseState.RUNNING
        self._timer.start()
        self.state_changed.emit(self._state)
        self.step_changed.emit(self._current_step_index)
        self.progress_updated.emit(0.0, 0.0)

    def _tick(self) -> None:
        """Timer tick — update progress and step transitions."""
        if self._state != ExerciseState.RUNNING:
            return

        overall = self.overall_progress
        step = self.step_progress or 0.0
        self.progress_updated.emit(overall, step)

        # Check for step transition
        elapsed = self._get_elapsed()
        self._advance_step_if_needed(elapsed)

        # Check for completion
        if overall >= 1.0:
            self._finish()

    def _advance_step_if_needed(self, elapsed: float) -> None:
        """Move to next step if we've passed the current step's end time."""
        steps = self._exercise.steps
        if self._current_step_index >= len(steps) - 1:
            return

        next_index = self._current_step_index + 1
        if next_index < len(self._step_start_offsets):
            next_offset = self._step_start_offsets[next_index]
            if elapsed >= next_offset:
                self._current_step_index = next_index
                self._step_start_time = time.monotonic()
                self._step_elapsed_at_pause = 0.0
                self.step_changed.emit(self._current_step_index)

    def _finish(self) -> None:
        """Exercise completed."""
        self._timer.stop()
        self._state = ExerciseState.COMPLETED
        self.progress_updated.emit(1.0, 1.0)
        self.state_changed.emit(self._state)
        self.completed.emit()

    def _get_elapsed(self) -> float:
        """Get total elapsed exercise time."""
        if self._start_time is None:
            return 0.0
        now = time.monotonic()
        elapsed = now - self._start_time
        if self._paused_at is not None:
            elapsed -= (now - self._paused_at)
        return elapsed

    def _get_step_elapsed(self) -> float:
        """Get elapsed time in current step."""
        if self._step_start_time is None:
            return 0.0
        now = time.monotonic()
        elapsed = now - self._step_start_time
        if self._paused_at is not None:
            elapsed = self._step_elapsed_at_pause
        return elapsed
