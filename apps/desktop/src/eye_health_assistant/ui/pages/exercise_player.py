"""Exercise player — guided exercise playback with animation, progress, and controls.

This is the primary screen users see while performing an exercise.
It displays the animation, current instruction, progress, and
pause/cancel controls.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.domain.models.exercise import (
    Exercise,
    ExerciseCompletion,
)
from eye_health_assistant.exercises.controller import (
    ExerciseController,
    ExerciseState,
)
from eye_health_assistant.ui.animations import (
    AnimationEngine,
    create_animation,
)

logger = logging.getLogger(__name__)


class ExercisePlayerPage(QWidget):
    """Full-screen exercise player with animation, instructions, and controls.

    Layout:
        Back
        ──────
        Exercise title

        Instruction

              ●
            visual
           target

        Progress bar / time remaining

        [ Pause ]    [ End ]
    """

    def __init__(
        self,
        exercise: Exercise,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._exercise = exercise
        self._controller = ExerciseController(exercise)
        self._animation: AnimationEngine | None = None
        self._completion_id = 0

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(0)

        # ── Header row ──
        header = QHBoxLayout()
        header.setSpacing(12)

        self._back_btn = QPushButton("← Back")
        self._back_btn.setObjectName("secondary-button")
        self._back_btn.clicked.connect(self._on_back)
        header.addWidget(self._back_btn)

        header.addStretch()

        layout.addLayout(header)

        # ── Title ──
        title = QLabel(self._exercise.title)
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        layout.addSpacing(8)

        # ── Countdown overlay (shown during countdown) ──
        self._countdown_label = QLabel("")
        self._countdown_label.setObjectName("timerDisplay")
        self._countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._countdown_label.hide()
        layout.addWidget(self._countdown_label)

        # ── Instruction ──
        self._instruction_label = QLabel("")
        self._instruction_label.setObjectName("subtitle")
        self._instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._instruction_label.setWordWrap(True)
        self._instruction_label.setMinimumHeight(48)
        layout.addWidget(self._instruction_label)

        layout.addSpacing(12)

        # ── Step indicator ──
        self._step_label = QLabel("")
        self._step_label.setObjectName("caption")
        self._step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._step_label)

        layout.addSpacing(8)

        # ── Animation area ──
        anim_container = QFrame()
        anim_container.setObjectName("card")
        anim_container.setFrameShape(QFrame.Shape.NoFrame)
        anim_container.setMinimumHeight(260)
        anim_container.setMaximumHeight(340)
        anim_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        anim_layout = QVBoxLayout(anim_container)
        anim_layout.setContentsMargins(0, 0, 0, 0)

        self._animation = create_animation(
            self._exercise.animation.type, parent=anim_container
        )
        anim_layout.addWidget(self._animation)

        layout.addWidget(anim_container, 1)

        layout.addSpacing(12)

        # ── Progress bar ──
        self._progress_frame = QFrame()
        self._progress_frame.setObjectName("card")
        self._progress_frame.setFrameShape(QFrame.Shape.NoFrame)
        prog_layout = QVBoxLayout(self._progress_frame)
        prog_layout.setContentsMargins(24, 16, 24, 16)
        prog_layout.setSpacing(8)

        # Time remaining
        self._time_label = QLabel("")
        self._time_label.setObjectName("stat-number")
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prog_layout.addWidget(self._time_label)

        # Progress bar (simple CSS-based)
        self._progress_bar = QLabel()
        self._progress_bar.setFixedHeight(6)
        self._progress_bar.setObjectName("progress-bar")
        self._progress_bar.setStyleSheet(
            "background-color: #E9ECEF; border-radius: 3px;"
        )
        prog_layout.addWidget(self._progress_bar)

        # Progress text
        self._progress_text = QLabel("0%")
        self._progress_text.setObjectName("caption")
        self._progress_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prog_layout.addWidget(self._progress_text)

        layout.addWidget(self._progress_frame)

        layout.addSpacing(16)

        # ── Controls ──
        controls = QHBoxLayout()
        controls.setSpacing(12)
        controls.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._pause_btn = QPushButton("Pause")
        self._pause_btn.setObjectName("secondary-button")
        self._pause_btn.setFixedWidth(120)
        self._pause_btn.clicked.connect(self._on_pause)
        controls.addWidget(self._pause_btn)

        self._cancel_btn = QPushButton("End")
        self._cancel_btn.setObjectName("danger-button")
        self._cancel_btn.setFixedWidth(120)
        self._cancel_btn.clicked.connect(self._on_cancel)
        controls.addWidget(self._cancel_btn)

        layout.addLayout(controls)

        # ── Completion screen (hidden initially) ──
        self._completion_widget = QWidget()
        comp_layout = QVBoxLayout(self._completion_widget)
        comp_layout.setContentsMargins(0, 40, 0, 0)
        comp_layout.setSpacing(16)
        comp_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        done_label = QLabel("Exercise complete")
        done_label.setObjectName("page-title")
        done_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        comp_layout.addWidget(done_label)

        msg = QLabel(self._exercise.completion_message)
        msg.setObjectName("subtitle")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        comp_layout.addWidget(msg)

        done_btn = QPushButton("Done")
        done_btn.setObjectName("primary-button")
        done_btn.setFixedWidth(160)
        done_btn.clicked.connect(self._on_back)
        comp_layout.addWidget(done_btn, 0, Qt.AlignmentFlag.AlignCenter)

        self._completion_widget.hide()
        layout.addWidget(self._completion_widget)

    def _connect_signals(self) -> None:
        c = self._controller
        c.state_changed.connect(self._on_state_changed)
        c.progress_updated.connect(self._on_progress)
        c.step_changed.connect(self._on_step_changed)
        c.countdown_tick.connect(self._on_countdown_tick)
        c.completed.connect(self._on_completed)

    # ── Start the exercise ──

    def start_exercise(self) -> None:
        """Begin the exercise (call after construction)."""
        self._controller.start()

    # ── Slots ──

    @Slot(object)
    def _on_state_changed(self, state: ExerciseState) -> None:
        if state == ExerciseState.RUNNING:
            self._countdown_label.hide()
            self._instruction_label.show()
            self._step_label.show()
            self._progress_frame.show()
            self._pause_btn.show()
            self._cancel_btn.show()
            self._back_btn.setEnabled(False)
        elif state == ExerciseState.PAUSED:
            self._pause_btn.setText("Resume")
            if self._animation:
                self._animation.pause()
        elif state == ExerciseState.COMPLETED:
            self._show_completion()
        elif state == ExerciseState.CANCELLED:
            self._on_back()

    @Slot(float, float)
    def _on_progress(self, overall: float, step: float) -> None:  # noqa: ARG002
        remaining = self._controller.remaining_seconds
        mins = int(remaining) // 60
        secs = int(remaining) % 60
        self._time_label.setText(f"{mins:02d}:{secs:02d} remaining")
        pct = int(overall * 100)
        self._progress_text.setText(f"{pct}%")
        self._update_progress_bar(overall)

    @Slot(int)
    def _on_step_changed(self, index: int) -> None:
        step = self._controller.current_step
        if step is None:
            return
        total = self._controller.total_steps
        self._step_label.setText(f"Step {index + 1} of {total}")
        self._instruction_label.setText(step.instruction)
        # Start animation for this step
        if self._animation:
            self._animation.start(step.duration_seconds)

    @Slot(int)
    def _on_countdown_tick(self, remaining: int) -> None:
        self._instruction_label.hide()
        self._step_label.hide()
        self._progress_frame.hide()
        self._pause_btn.hide()
        self._cancel_btn.hide()
        self._countdown_label.show()
        if remaining > 0:
            self._countdown_label.setText(str(remaining))
        else:
            self._countdown_label.setText("Go")
            self._countdown_label.hide()

    def _on_pause(self) -> None:
        if self._controller.state == ExerciseState.RUNNING:
            self._controller.pause()
        elif self._controller.state == ExerciseState.PAUSED:
            self._controller.resume()
            self._pause_btn.setText("Pause")
            if self._animation:
                self._animation.resume()

    def _on_cancel(self) -> None:
        self._controller.cancel()
        self._on_back()

    def _on_back(self) -> None:
        """Clean up and emit navigation signal."""
        if self._animation:
            self._animation.cleanup()
        self._controller.reset()
        # Find the parent ExercisesPage and show list
        parent = self.parent()
        if parent is not None and hasattr(parent, "_show_list"):
            parent._show_list()

    def _on_completed(self) -> None:
        """Record exercise completion."""
        self._completion_id += 1
        now = datetime.now(UTC)
        completion = ExerciseCompletion(
            id=f"ex-comp-{self._completion_id}",
            exercise_id=self._exercise.id,
            exercise_slug=self._exercise.slug,
            started_at=now,
            completed_at=now,
            duration_seconds=self._exercise.duration_seconds,
        )
        logger.info("Exercise completed: %s", completion.exercise_slug)

    def _show_completion(self) -> None:
        """Show completion screen."""
        if self._animation:
            self._animation.stop()
        self._instruction_label.hide()
        self._step_label.hide()
        self._progress_frame.hide()
        self._pause_btn.hide()
        self._cancel_btn.hide()
        self._completion_widget.show()

    def _update_progress_bar(self, progress: float) -> None:
        """Update the CSS-based progress bar."""
        pct = max(0, min(100, int(progress * 100)))
        self._progress_bar.setStyleSheet(
            f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            f"stop:0 #3B82F6 {pct}%, stop:{pct}% #E9ECEF {pct}%, "
            f"stop:100% #E9ECEF 100%); border-radius: 3px;"
        )

    # ── Keyboard ──

    def keyPressEvent(self, event: object) -> None:  # noqa: N802
        """Handle keyboard shortcuts."""
        from PySide6.QtGui import QKeyEvent

        if isinstance(event, QKeyEvent):
            if event.key() == Qt.Key.Key_Space:
                self._on_pause()
                return
            if event.key() == Qt.Key.Key_Escape:
                self._on_cancel()
                return
        super().keyPressEvent(event)  # type: ignore[arg-type]
