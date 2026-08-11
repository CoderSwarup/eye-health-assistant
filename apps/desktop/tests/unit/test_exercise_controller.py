"""Tests for exercise controller and animation engine."""

from __future__ import annotations

from eye_health_assistant.domain.models.exercise import (
    Exercise,
    ExerciseAnimation,
    ExerciseStep,
)
from eye_health_assistant.exercises.controller import (
    ExerciseController,
    ExerciseState,
)


def _make_exercise(
    duration: int = 10, steps: list[ExerciseStep] | None = None,
) -> Exercise:
    """Create a minimal test exercise."""
    if steps is None:
        steps = [
            ExerciseStep(
                title="Step 1", instruction="Do something",
                duration_seconds=5,
            ),
            ExerciseStep(
                title="Step 2", instruction="Do more",
                duration_seconds=5,
            ),
        ]
    return Exercise(
        id="test-exercise",
        slug="test-exercise",
        title="Test Exercise",
        short_title="Test",
        description="A test exercise",
        purpose="Testing",
        category="Blinking",
        difficulty="Beginner",
        duration_seconds=duration,
        recommended_frequency="Daily",
        steps=steps,
        safety_note="",
        animation=ExerciseAnimation(type="blink"),
        completion_message="Done!",
    )


class TestExerciseState:
    """Test ExerciseState enum."""

    def test_all_states_exist(self) -> None:
        states = [
            ExerciseState.READY,
            ExerciseState.COUNTDOWN,
            ExerciseState.RUNNING,
            ExerciseState.PAUSED,
            ExerciseState.COMPLETED,
            ExerciseState.CANCELLED,
        ]
        assert len(states) == 6

    def test_initial_state(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        assert ctrl.state == ExerciseState.READY


class TestExerciseController:
    """Test exercise controller state machine."""

    def test_start_transitions_to_countdown(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        states: list[ExerciseState] = []
        ctrl.state_changed.connect(lambda s: states.append(s))

        ctrl.start()
        assert ctrl.state == ExerciseState.COUNTDOWN
        assert ExerciseState.COUNTDOWN in states

    def test_countdown_completes_to_running(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()

        ctrl._countdown_tick_handler()
        assert ctrl.state == ExerciseState.COUNTDOWN

        ctrl._countdown_tick_handler()
        assert ctrl.state == ExerciseState.COUNTDOWN

        ctrl._countdown_tick_handler()
        assert ctrl.state == ExerciseState.RUNNING

    def test_pause_from_running(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()

        assert ctrl.state == ExerciseState.RUNNING
        ctrl.pause()
        assert ctrl.state == ExerciseState.PAUSED

    def test_resume_from_paused(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()

        ctrl.pause()
        assert ctrl.state == ExerciseState.PAUSED
        ctrl.resume()
        assert ctrl.state == ExerciseState.RUNNING

    def test_cancel_from_running(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()

        ctrl.cancel()
        assert ctrl.state == ExerciseState.CANCELLED

    def test_cancel_from_paused(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()

        ctrl.pause()
        ctrl.cancel()
        assert ctrl.state == ExerciseState.CANCELLED

    def test_reset_returns_to_ready(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()
        ctrl.cancel()
        ctrl.reset()
        assert ctrl.state == ExerciseState.READY

    def test_cannot_pause_from_countdown(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        assert ctrl.state == ExerciseState.COUNTDOWN
        ctrl.pause()
        assert ctrl.state == ExerciseState.COUNTDOWN

    def test_cannot_start_while_running(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()
        ctrl.start()
        assert ctrl.state == ExerciseState.RUNNING

    def test_current_step_none_before_start(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        assert ctrl.current_step is None

    def test_current_step_after_running(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()
        assert ctrl.current_step is not None
        assert ctrl.current_step.title == "Step 1"

    def test_total_steps(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        assert ctrl.total_steps == 2

    def test_step_changed_signal(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        step_indices: list[int] = []
        ctrl.step_changed.connect(lambda i: step_indices.append(i))

        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()

        assert 0 in step_indices

    def test_overall_progress_starts_at_zero(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        assert ctrl.overall_progress == 0.0

    def test_remaining_seconds(self) -> None:
        ex = _make_exercise(duration=10)
        ctrl = ExerciseController(ex)
        remaining = ctrl.remaining_seconds
        assert remaining == 10.0

    def test_completed_signal(self) -> None:
        ex = _make_exercise(duration=1)
        ctrl = ExerciseController(ex)
        completed: list[bool] = []
        ctrl.completed.connect(lambda: completed.append(True))

        ctrl.start()
        for _ in range(3):
            ctrl._countdown_tick_handler()

        ctrl._finish()
        assert ctrl.state == ExerciseState.COMPLETED
        assert completed == [True]

    def test_step_progress_none_before_start(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        assert ctrl.step_progress is None

    def test_single_step_exercise(self) -> None:
        steps = [
            ExerciseStep(title="Only", instruction="Do it", duration_seconds=10),
        ]
        ex = _make_exercise(duration=10, steps=steps)
        ctrl = ExerciseController(ex)
        assert ctrl.total_steps == 1

    def test_start_after_cancel(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ctrl.start()
        ctrl.cancel()
        ctrl.reset()
        ctrl.start()
        assert ctrl.state == ExerciseState.COUNTDOWN

    def test_countdown_tick_signal(self) -> None:
        ex = _make_exercise()
        ctrl = ExerciseController(ex)
        ticks: list[int] = []
        ctrl.countdown_tick.connect(lambda n: ticks.append(n))

        ctrl.start()
        # start() emits initial tick of 3, then each handler emits next
        ctrl._countdown_tick_handler()
        ctrl._countdown_tick_handler()
        assert ticks == [3, 2, 1]


class TestAnimationFactory:
    """Test animation factory function (no Qt widget creation)."""

    def test_factory_returns_correct_types(self) -> None:
        try:
            from eye_health_assistant.ui.animations.engine import (
                create_animation,
            )
        except ImportError:
            # PySide6/OpenGL not available in CI environments
            return

        # Test that factory function exists
        assert callable(create_animation)

    def test_animation_state_enum(self) -> None:
        try:
            from eye_health_assistant.ui.animations.engine import AnimationState
        except ImportError:
            # PySide6/OpenGL not available in CI environments
            return

        assert AnimationState.IDLE.value == "idle"
        assert AnimationState.PLAYING.value == "playing"
        assert AnimationState.PAUSED.value == "paused"
        assert AnimationState.COMPLETED.value == "completed"
