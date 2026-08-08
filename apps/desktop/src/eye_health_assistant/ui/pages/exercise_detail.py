"""Exercise detail page — structured exercise view with steps and metadata."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.content.loader import get_related_articles
from eye_health_assistant.core.result import Err
from eye_health_assistant.domain.models.exercise import Exercise


class ExerciseDetailPage(QWidget):
    """Full detail view for a single exercise."""

    back_clicked = Signal()

    def __init__(self, exercise: Exercise, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.exercise = exercise
        self._build_ui()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("secondary-button")
        back_btn.clicked.connect(self.back_clicked.emit)
        layout.addWidget(back_btn)

        # Title
        title = QLabel(self.exercise.title)
        title.setObjectName("page-title")
        layout.addWidget(title)

        # Meta row
        meta = QHBoxLayout()
        meta.setSpacing(16)

        category_label = QLabel(self.exercise.category)
        category_label.setObjectName("caption")
        meta.addWidget(category_label)

        duration_label = QLabel(f"{self.exercise.duration_seconds}s")
        duration_label.setObjectName("caption")
        meta.addWidget(duration_label)

        difficulty_label = QLabel(self.exercise.difficulty)
        difficulty_label.setObjectName("caption")
        meta.addWidget(difficulty_label)

        meta.addStretch()
        layout.addLayout(meta)

        # Purpose card
        if self.exercise.purpose:
            purpose_card = QFrame()
            purpose_card.setObjectName("card")
            purpose_card.setFrameShape(QFrame.Shape.NoFrame)

            purpose_layout = QVBoxLayout(purpose_card)
            purpose_layout.setContentsMargins(0, 0, 0, 0)
            purpose_layout.setSpacing(8)

            purpose_title = QLabel("Purpose")
            purpose_title.setObjectName("section-title")
            purpose_layout.addWidget(purpose_title)

            purpose_text = QLabel(self.exercise.purpose)
            purpose_text.setObjectName("subtitle")
            purpose_text.setWordWrap(True)
            purpose_layout.addWidget(purpose_text)

            layout.addWidget(purpose_card)

        # Description card
        desc_card = QFrame()
        desc_card.setObjectName("card")
        desc_card.setFrameShape(QFrame.Shape.NoFrame)

        desc_layout = QVBoxLayout(desc_card)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(8)

        desc_title = QLabel("About")
        desc_title.setObjectName("section-title")
        desc_layout.addWidget(desc_title)

        desc_text = QLabel(self.exercise.description)
        desc_text.setObjectName("subtitle")
        desc_text.setWordWrap(True)
        desc_layout.addWidget(desc_text)

        layout.addWidget(desc_card)

        # Steps card
        if self.exercise.steps:
            steps_card = QFrame()
            steps_card.setObjectName("card")
            steps_card.setFrameShape(QFrame.Shape.NoFrame)

            steps_layout = QVBoxLayout(steps_card)
            steps_layout.setContentsMargins(0, 0, 0, 0)
            steps_layout.setSpacing(12)

            steps_title = QLabel("Steps")
            steps_title.setObjectName("section-title")
            steps_layout.addWidget(steps_title)

            for i, step in enumerate(self.exercise.steps, 1):
                step_row = QHBoxLayout()
                step_row.setSpacing(12)

                num_label = QLabel(f"{i}.")
                num_label.setObjectName("stat-number")
                num_label.setFixedWidth(30)
                step_row.addWidget(num_label)

                step_info = QVBoxLayout()
                step_info.setSpacing(2)

                step_title = QLabel(step.title)
                step_title.setObjectName("subtitle")
                step_info.addWidget(step_title)

                step_inst = QLabel(step.instruction)
                step_inst.setObjectName("caption")
                step_inst.setWordWrap(True)
                step_info.addWidget(step_inst)

                step_row.addLayout(step_info, 1)

                step_dur = QLabel(f"{step.duration_seconds}s")
                step_dur.setObjectName("caption")
                step_row.addWidget(step_dur)

                steps_layout.addLayout(step_row)

            layout.addWidget(steps_card)

        # Safety note
        if self.exercise.safety_note:
            safety_card = QFrame()
            safety_card.setObjectName("card")
            safety_card.setFrameShape(QFrame.Shape.NoFrame)

            safety_layout = QVBoxLayout(safety_card)
            safety_layout.setContentsMargins(0, 0, 0, 0)
            safety_layout.setSpacing(8)

            safety_title = QLabel("Safety Note")
            safety_title.setObjectName("section-title")
            safety_layout.addWidget(safety_title)

            safety_text = QLabel(self.exercise.safety_note)
            safety_text.setObjectName("subtitle")
            safety_text.setWordWrap(True)
            safety_layout.addWidget(safety_text)

            layout.addWidget(safety_card)

        # Recommended frequency
        if self.exercise.recommended_frequency:
            freq_label = QLabel(
                f"Recommended: {self.exercise.recommended_frequency}"
            )
            freq_label.setObjectName("caption")
            layout.addWidget(freq_label)

        # Related articles
        if self.exercise.related_articles:
            self._add_related_articles(layout)

        # Start button
        start_btn = QPushButton("Start Exercise")
        layout.addWidget(start_btn)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

    def _add_related_articles(self, layout: QVBoxLayout) -> None:
        """Add related articles section."""
        result = get_related_articles(self.exercise.slug)
        if isinstance(result, Err) or not result.value:
            return

        articles = result.value

        related_card = QFrame()
        related_card.setObjectName("card")
        related_card.setFrameShape(QFrame.Shape.NoFrame)

        related_layout = QVBoxLayout(related_card)
        related_layout.setContentsMargins(0, 0, 0, 0)
        related_layout.setSpacing(8)

        related_title = QLabel("Related Articles")
        related_title.setObjectName("section-title")
        related_layout.addWidget(related_title)

        for article in articles:
            article_row = QHBoxLayout()
            article_row.setSpacing(12)

            name_label = QLabel(article.title)
            name_label.setObjectName("subtitle")
            article_row.addWidget(name_label)

            article_row.addStretch()

            time_label = QLabel(f"{article.reading_time_minutes} min")
            time_label.setObjectName("caption")
            article_row.addWidget(time_label)

            related_layout.addLayout(article_row)

        layout.addWidget(related_card)
