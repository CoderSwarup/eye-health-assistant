"""Eye Care page — articles with filtering and detail navigation."""

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
    get_article_categories,
    load_articles,
)
from eye_health_assistant.core.result import Err
from eye_health_assistant.domain.models.article import Article
from eye_health_assistant.ui.pages.article_detail import ArticleDetailPage

logger = logging.getLogger(__name__)


class ArticleCard(QFrame):
    """Card displaying a single article."""

    clicked = Signal(object)

    def __init__(self, article: Article, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.article = article
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = QHBoxLayout()
        header.setSpacing(12)

        title_label = QLabel(article.title)
        title_label.setObjectName("section-title")
        header.addWidget(title_label)
        header.addStretch()

        category_label = QLabel(article.category)
        category_label.setObjectName("caption")
        header.addWidget(category_label)

        layout.addLayout(header)

        meta_row = QHBoxLayout()
        meta_row.setSpacing(16)

        read_time_label = QLabel(f"{article.reading_time_minutes} min read")
        read_time_label.setObjectName("caption")
        meta_row.addWidget(read_time_label)

        if article.tags:
            tags_label = QLabel("  ".join(f"#{t}" for t in article.tags[:3]))
            tags_label.setObjectName("caption")
            meta_row.addWidget(tags_label)

        meta_row.addStretch()
        layout.addLayout(meta_row)

        summary_label = QLabel(article.summary)
        summary_label.setObjectName("subtitle")
        summary_label.setWordWrap(True)
        layout.addWidget(summary_label)

        read_btn = QPushButton("Read Article")
        read_btn.setObjectName("secondary-button")
        read_btn.clicked.connect(lambda: self.clicked.emit(article))
        layout.addWidget(read_btn)


class EyeCarePage(QWidget):
    """Eye care education page with category filtering and stacked list/detail views."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._stack = QStackedWidget()
        self._list_index = 0
        self._detail_index = 1
        self._all_articles: list[Article] = []
        self._current_category: str | None = None
        self._grid_layout: QGridLayout | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # List view
        list_widget = QWidget()
        self._list_layout = QVBoxLayout(list_widget)
        self._list_layout.setContentsMargins(36, 28, 36, 28)
        self._list_layout.setSpacing(28)

        title = QLabel("Eye Care")
        title.setObjectName("page-title")
        self._list_layout.addWidget(title)

        subtitle = QLabel(
            "Learn about eye health, screen habits, and wellness tips."
        )
        subtitle.setObjectName("subtitle")
        self._list_layout.addWidget(subtitle)

        # Category filter buttons
        self._filter_layout = QHBoxLayout()
        self._filter_layout.setSpacing(10)
        self._list_layout.addLayout(self._filter_layout)

        # Articles grid container
        self._grid_container = QWidget()
        self._grid_layout = QGridLayout(self._grid_container)
        self._grid_layout.setSpacing(16)
        self._list_layout.addWidget(self._grid_container)

        self._list_layout.addStretch()

        # Load articles
        result = load_articles()
        if isinstance(result, Err):
            logger.error("Failed to load articles: %s", result.error)
            error_label = QLabel("Could not load articles.")
            error_label.setObjectName("subtitle")
            self._list_layout.insertWidget(3, error_label)
        else:
            self._all_articles = result.value
            self._build_category_filters()
            self._render_articles()

        self._stack.addWidget(list_widget)
        self._list_index = 0

        # Detail placeholder
        detail_placeholder = QWidget()
        self._stack.addWidget(detail_placeholder)
        self._detail_index = 1

        layout.addWidget(self._stack)

    def _build_category_filters(self) -> None:
        """Build category filter buttons."""
        all_btn = QPushButton("All")
        all_btn.setObjectName("secondary-button")
        all_btn.clicked.connect(lambda: self._filter_by_category(None))
        self._filter_layout.addWidget(all_btn)

        cats_result = get_article_categories()
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
        """Filter articles by category."""
        self._current_category = category
        self._render_articles()

    def _render_articles(self) -> None:
        """Render the article grid with current filter."""
        if self._grid_layout is None:
            return

        # Clear existing cards
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()

        filtered = self._all_articles
        if self._current_category is not None:
            filtered = [a for a in filtered if a.category == self._current_category]

        for i, article in enumerate(filtered):
            card = ArticleCard(article)
            card.clicked.connect(self._show_detail)
            self._grid_layout.addWidget(card, i // 2, i % 2)

    def _show_detail(self, article: Article) -> None:
        """Show the detail view for an article."""
        detail = ArticleDetailPage(article)
        detail.back_clicked.connect(self._show_list)

        old = self._stack.widget(self._detail_index)
        if old is not None:
            self._stack.removeWidget(old)
            old.deleteLater()
        self._stack.insertWidget(self._detail_index, detail)
        self._stack.setCurrentIndex(self._detail_index)

    def _show_list(self) -> None:
        """Return to the list view."""
        self._stack.setCurrentIndex(self._list_index)
