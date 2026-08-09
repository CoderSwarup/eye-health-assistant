"""Exercises page — catalog with filtering, detail, and player navigation."""

from __future__ import annotations

import logging

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies
from eye_health_assistant.content.loader import (
    get_exercise_categories,
    load_exercises,
)
from eye_health_assistant.core.result import Err
from eye_health_assistant.domain.models.exercise import Exercise
from eye_health_assistant.ui.pages.exercise_detail import ExerciseDetailPage
from eye_health_assistant.ui.pages.exercise_player import ExercisePlayerPage

logger = logging.getLogger(__name__)


class ExerciseCard(QFrame):
    """Card displaying a single exercise."""

    clicked = Signal(object)

    def __init__(self, exercise: Exercise, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.exercise = exercise
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(160)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = QHBoxLayout()
        header.setSpacing(12)

        name_label = QLabel(exercise.title)
        name_label.setObjectName("section-title")
        header.addWidget(name_label)
        header.addStretch()

        difficulty_label = QLabel(exercise.difficulty)
        difficulty_label.setObjectName("caption")
        header.addWidget(difficulty_label)

        layout.addLayout(header)

        meta_row = QHBoxLayout()
        meta_row.setSpacing(16)

        category_label = QLabel(exercise.category)
        category_label.setObjectName("caption")
        meta_row.addWidget(category_label)

        duration_label = QLabel(f"{exercise.duration_seconds}s")
        duration_label.setObjectName("caption")
        meta_row.addWidget(duration_label)

        meta_row.addStretch()
        layout.addLayout(meta_row)

        desc_label = QLabel(exercise.description)
        desc_label.setObjectName("subtitle")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        start_btn = QPushButton("Start Exercise")
        start_btn.clicked.connect(lambda: self.clicked.emit(exercise))
        layout.addWidget(start_btn)


class ExercisesPage(QWidget):
    """Exercise catalog with category filtering and list/detail/player views."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._stack = QStackedWidget()
        self._list_index = 0
        self._detail_index = 1
        self._player_index = 2
        self._all_exercises: list[Exercise] = []
        self._current_category: str | None = None
        self._grid_layout: QGridLayout | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── List view ──
        list_widget = QWidget()
        self._list_layout = QVBoxLayout(list_widget)
        self._list_layout.setContentsMargins(36, 28, 36, 28)
        self._list_layout.setSpacing(28)

        title = QLabel("Exercises")
        title.setObjectName("page-title")
        self._list_layout.addWidget(title)

        subtitle = QLabel(
            "Short guided visual-rest activities to reduce eye strain."
        )
        subtitle.setObjectName("subtitle")
        self._list_layout.addWidget(subtitle)

        # Category filter buttons
        self._filter_layout = QHBoxLayout()
        self._filter_layout.setSpacing(10)
        self._list_layout.addLayout(self._filter_layout)

        # Exercises grid container
        self._grid_container = QWidget()
        self._grid_layout = QGridLayout(self._grid_container)
        self._grid_layout.setSpacing(16)
        self._list_layout.addWidget(self._grid_container)

        self._list_layout.addStretch()

        # Load exercises
        result = load_exercises()
        if isinstance(result, Err):
            logger.error("Failed to load exercises: %s", result.error)
            error_label = QLabel("Could not load exercises.")
            error_label.setObjectName("subtitle")
            self._list_layout.insertWidget(3, error_label)
        else:
            self._all_exercises = result.value
            self._build_category_filters()
            self._render_exercises()

        self._stack.addWidget(list_widget)
        self._list_index = 0

        # ── Detail placeholder ──
        detail_placeholder = QWidget()
        self._stack.addWidget(detail_placeholder)
        self._detail_index = 1

        # ── Player placeholder ──
        player_placeholder = QWidget()
        self._stack.addWidget(player_placeholder)
        self._player_index = 2

        layout.addWidget(self._stack)

    def _build_category_filters(self) -> None:
        """Build category filter buttons."""
        all_btn = QPushButton("All")
        all_btn.setObjectName("secondary-button")
        all_btn.clicked.connect(lambda: self._filter_by_category(None))
        self._filter_layout.addWidget(all_btn)

        cats_result = get_exercise_categories()
        if isinstance(cats_result, Err):
            return

        for category in cats_result.value:
            btn = QPushButton(category)
            btn.setObjectName("secondary-button")
            btn.clicked.connect(
                lambda _checked, cat=category: self._filter_by_category(cat)
            )
            self._filter_layout.addWidget(btn)

        self._filter_layout.addStretch()

    def _filter_by_category(self, category: str | None) -> None:
        """Filter exercises by category."""
        self._current_category = category
        self._render_exercises()

    def _render_exercises(self) -> None:
        """Render the exercise grid with current filter."""
        if self._grid_layout is None:
            return

        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()

        filtered = self._all_exercises
        if self._current_category is not None:
            filtered = [e for e in filtered if e.category == self._current_category]

        for i, exercise in enumerate(filtered):
            card = ExerciseCard(exercise)
            card.clicked.connect(self._show_detail)
            self._grid_layout.addWidget(card, i // 2, i % 2)

    def _show_detail(self, exercise: Exercise) -> None:
        """Show the detail view for an exercise."""
        detail = ExerciseDetailPage(exercise)
        detail.back_clicked.connect(self._show_list)
        detail.start_clicked.connect(lambda e=exercise: self._start_exercise(e))

        old = self._stack.widget(self._detail_index)
        if old is not None:
            self._stack.removeWidget(old)
            old.deleteLater()
        self._stack.insertWidget(self._detail_index, detail)
        self._stack.setCurrentIndex(self._detail_index)

    def _start_exercise(self, exercise: Exercise) -> None:
        """Show the exercise player for the given exercise."""
        player = ExercisePlayerPage(exercise, parent=self)
        old = self._stack.widget(self._player_index)
        if old is not None:
            self._stack.removeWidget(old)
            old.deleteLater()
        self._stack.insertWidget(self._player_index, player)
        self._stack.setCurrentIndex(self._player_index)
        player.start_exercise()

    def _show_list(self) -> None:
        """Return to the list view."""
        self._stack.setCurrentIndex(self._list_index)
