"""Article detail page — full structured article content view."""

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

from eye_health_assistant.content.loader import get_related_exercises
from eye_health_assistant.core.result import Err
from eye_health_assistant.domain.models.article import Article


class ArticleDetailPage(QWidget):
    """Full detail view for a single article."""

    back_clicked = Signal()

    def __init__(self, article: Article, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.article = article
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

        # Category
        cat_label = QLabel(self.article.category)
        cat_label.setObjectName("caption")
        layout.addWidget(cat_label)

        # Title
        title = QLabel(self.article.title)
        title.setObjectName("page-title")
        layout.addWidget(title)

        # Summary
        summary = QLabel(self.article.summary)
        summary.setObjectName("subtitle")
        summary.setWordWrap(True)
        layout.addWidget(summary)

        # Meta row
        meta = QHBoxLayout()
        meta.setSpacing(16)
        time_label = QLabel(f"{self.article.reading_time_minutes} min read")
        time_label.setObjectName("caption")
        meta.addWidget(time_label)
        if self.article.tags:
            tags_label = QLabel("  ".join(f"#{t}" for t in self.article.tags[:4]))
            tags_label.setObjectName("caption")
            meta.addWidget(tags_label)
        meta.addStretch()
        layout.addLayout(meta)

        # Article sections
        for section in self.article.sections:
            section_card = QFrame()
            section_card.setObjectName("card")
            section_card.setFrameShape(QFrame.Shape.NoFrame)

            section_layout = QVBoxLayout(section_card)
            section_layout.setContentsMargins(0, 0, 0, 0)
            section_layout.setSpacing(8)

            section_title = QLabel(section.title)
            section_title.setObjectName("section-title")
            section_layout.addWidget(section_title)

            section_content = QLabel(section.content)
            section_content.setObjectName("subtitle")
            section_content.setWordWrap(True)
            section_layout.addWidget(section_content)

            layout.addWidget(section_card)

        # Quick tips
        if self.article.quick_tips:
            tips_card = QFrame()
            tips_card.setObjectName("card")
            tips_card.setFrameShape(QFrame.Shape.NoFrame)

            tips_layout = QVBoxLayout(tips_card)
            tips_layout.setContentsMargins(0, 0, 0, 0)
            tips_layout.setSpacing(8)

            tips_title = QLabel("Quick Tips")
            tips_title.setObjectName("section-title")
            tips_layout.addWidget(tips_title)

            for tip in self.article.quick_tips:
                tip_label = QLabel(f"  {tip}")
                tip_label.setObjectName("subtitle")
                tip_label.setWordWrap(True)
                tips_layout.addWidget(tip_label)

            layout.addWidget(tips_card)

        # Related exercises
        if self.article.related_exercises:
            self._add_related_exercises(layout)

        # Sources
        if self.article.sources:
            sources_card = QFrame()
            sources_card.setObjectName("card")
            sources_card.setFrameShape(QFrame.Shape.NoFrame)

            sources_layout = QVBoxLayout(sources_card)
            sources_layout.setContentsMargins(0, 0, 0, 0)
            sources_layout.setSpacing(8)

            sources_title = QLabel("Sources")
            sources_title.setObjectName("section-title")
            sources_layout.addWidget(sources_title)

            for source in self.article.sources:
                source_text = f"{source.organization}"
                if source.title:
                    source_text = f"{source.title} — {source_text}"
                if source.published_at:
                    source_text += f" ({source.published_at})"
                source_label = QLabel(source_text)
                source_label.setObjectName("caption")
                source_label.setWordWrap(True)
                sources_layout.addWidget(source_label)

            layout.addWidget(sources_card)

        # Disclaimer
        if self.article.disclaimer:
            disclaimer_label = QLabel(self.article.disclaimer)
            disclaimer_label.setObjectName("caption")
            disclaimer_label.setWordWrap(True)
            layout.addWidget(disclaimer_label)

        layout.addStretch()
        scroll.setWidget(content)
        outer.addWidget(scroll)

    def _add_related_exercises(self, layout: QVBoxLayout) -> None:
        """Add related exercises section."""
        result = get_related_exercises(self.article.slug)
        if isinstance(result, Err) or not result.value:
            return

        exercises = result.value

        related_card = QFrame()
        related_card.setObjectName("card")
        related_card.setFrameShape(QFrame.Shape.NoFrame)

        related_layout = QVBoxLayout(related_card)
        related_layout.setContentsMargins(0, 0, 0, 0)
        related_layout.setSpacing(8)

        related_title = QLabel("Related Exercises")
        related_title.setObjectName("section-title")
        related_layout.addWidget(related_title)

        for exercise in exercises:
            exercise_row = QHBoxLayout()
            exercise_row.setSpacing(12)

            name_label = QLabel(exercise.title)
            name_label.setObjectName("subtitle")
            exercise_row.addWidget(name_label)

            exercise_row.addStretch()

            duration_label = QLabel(f"{exercise.duration_seconds}s")
            duration_label.setObjectName("caption")
            exercise_row.addWidget(duration_label)

            related_layout.addLayout(exercise_row)

        layout.addWidget(related_card)
