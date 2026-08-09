"""Statistics page — usage metrics, trends, and charts."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.analytics.service import (
    ComparisonResult,
    PeriodSummary,
    TimePeriod,
)
from eye_health_assistant.app.dependencies import Dependencies
from eye_health_assistant.ui.charts import (
    BarChartWidget,
    ChartDataPoint,
    ChartSeries,
    LineChartWidget,
    SummaryCard,
)


class StatisticsPage(QWidget):
    """Statistics and analytics page with charts."""

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._current_period = TimePeriod.WEEK
        self._summary_cards: list[SummaryCard] = []
        self._activity_chart: BarChartWidget | None = None
        self._blink_chart: LineChartWidget | None = None
        self._period_btns: list[QPushButton] = []
        self._build_ui()
        self._load_statistics()

    def _build_ui(self) -> None:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(36, 28, 36, 28)
        layout.setSpacing(28)

        # Header
        header = QHBoxLayout()
        title = QLabel("Statistics")
        title.setObjectName("page-title")
        header.addWidget(title)
        header.addStretch()

        # Period selector
        period_layout = QHBoxLayout()
        period_layout.setSpacing(10)
        for label, period in [
            ("Today", TimePeriod.TODAY),
            ("7 Days", TimePeriod.WEEK),
            ("30 Days", TimePeriod.MONTH),
        ]:
            btn = QPushButton(label)
            btn.setObjectName("secondary-button")
            btn.clicked.connect(
                lambda _checked, p=period: self._on_period_changed(p)
            )
            period_layout.addWidget(btn)
            self._period_btns.append(btn)
        header.addLayout(period_layout)

        layout.addLayout(header)

        # Summary metrics
        self._summary_container = QHBoxLayout()
        self._summary_container.setSpacing(16)
        layout.addLayout(self._summary_container)

        # Charts section
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(16)

        self._activity_chart = BarChartWidget("Activity Overview")
        charts_layout.addWidget(self._activity_chart)

        self._blink_chart = LineChartWidget("Blink Rate Trend")
        charts_layout.addWidget(self._blink_chart)

        layout.addLayout(charts_layout)

        # Comparison section
        self._comparison_frame = QFrame()
        self._comparison_frame.setObjectName("card")
        self._comparison_frame.setFrameShape(QFrame.Shape.NoFrame)
        self._comparison_layout = QVBoxLayout(self._comparison_frame)
        self._comparison_layout.setContentsMargins(0, 0, 0, 0)
        self._comparison_layout.setSpacing(8)
        layout.addWidget(self._comparison_frame)

        # Export button
        export_btn = QPushButton("Export Data (JSON)")
        export_btn.setObjectName("secondary-button")
        export_btn.clicked.connect(self._on_export)
        layout.addWidget(export_btn)

        # Delete button
        delete_btn = QPushButton("Delete All Data")
        delete_btn.setObjectName("danger-button")
        delete_btn.clicked.connect(self._on_delete_all)
        layout.addWidget(delete_btn)

        # Privacy note
        privacy_label = QLabel(
            "Your activity history is stored locally on this device."
        )
        privacy_label.setObjectName("caption")
        privacy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(privacy_label)

        layout.addStretch()

        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _on_period_changed(self, period: TimePeriod) -> None:
        """Handle period selector change."""
        self._current_period = period
        self._load_statistics()

    def _load_statistics(self) -> None:
        """Load statistics from the analytics service."""
        if self.deps.analytics_service is None:
            self._show_placeholder_stats()
            return

        service = self.deps.analytics_service
        summary = service.get_summary(self._current_period)
        comparison = service.get_comparison(self._current_period)
        daily = service.get_daily_trend(self._current_period)

        # Update summary cards
        self._update_summary_cards(summary, comparison)

        # Update charts
        self._update_activity_chart(daily)
        self._update_blink_chart(daily)

        # Update comparison
        self._update_comparison(comparison)

    def _update_summary_cards(
        self,
        summary: PeriodSummary,
        _comparison: ComparisonResult | None,
    ) -> None:
        """Update the summary metric cards."""
        # Clear existing cards
        while self._summary_container.count():
            item = self._summary_container.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        self._summary_cards.clear()

        period_label = {
            TimePeriod.TODAY: "Today",
            TimePeriod.WEEK: "This Week",
            TimePeriod.MONTH: "This Month",
            TimePeriod.ALL: "All Time",
        }.get(summary.period, "")

        cards_data = [
            ("Focus Time", summary.focus_hours_display, period_label),
            ("Break Time", summary.break_hours_display, period_label),
            ("Breaks Completed", str(summary.focus_sessions_completed), period_label),
            ("Smart Monitoring", summary.monitoring_hours_display, period_label),
            ("Estimated Blink Rate", summary.blink_rate_display, period_label),
            ("Active Days", str(summary.active_days), period_label),
        ]

        for title, value, subtitle in cards_data:
            card = SummaryCard(title, value, subtitle)
            self._summary_container.addWidget(card)
            self._summary_cards.append(card)

    def _update_activity_chart(self, daily: list) -> None:
        """Update the activity bar chart."""
        if self._activity_chart is None:
            return

        points = []
        for d in daily[-7:]:  # Last 7 days
            label = d.date.strftime("%a")
            points.append(
                ChartDataPoint(
                    label=label,
                    value=d.focus_seconds / 60.0,  # Convert to minutes
                )
            )

        if points:
            self._activity_chart.set_data(
                ChartSeries(name="Focus Minutes", points=points, color="#4A90D9")
            )
        else:
            self._activity_chart.set_data(
                ChartSeries(name="No Data", points=[])
            )

    def _update_blink_chart(self, daily: list) -> None:
        """Update the blink rate line chart."""
        if self._blink_chart is None:
            return

        points = []
        for d in daily[-7:]:  # Last 7 days
            label = d.date.strftime("%a")
            rate = d.avg_blink_rate if d.avg_blink_rate else 0.0
            points.append(ChartDataPoint(label=label, value=rate))

        if points:
            self._blink_chart.set_data([
                ChartSeries(name="Blink Rate", points=points, color="#E8913A")
            ])
        else:
            self._blink_chart.set_data([
                ChartSeries(name="No Data", points=[])
            ])

    def _update_comparison(self, comparison: ComparisonResult | None) -> None:
        """Update the comparison section."""
        if self._comparison_frame is None:
            return

        # Clear existing
        while self._comparison_layout.count():
            item = self._comparison_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        if comparison is None:
            return

        title = QLabel("Period Comparison")
        title.setObjectName("section-title")
        self._comparison_layout.addWidget(title)

        focus_pct = comparison.focus_change_pct
        break_pct = comparison.break_change_pct

        messages = []
        if focus_pct is not None:
            direction = "increased" if focus_pct > 0 else "decreased"
            messages.append(
                f"Focus time {direction} by {abs(focus_pct):.0f}% "
                "compared to previous period."
            )
        if break_pct is not None:
            direction = "increased" if break_pct > 0 else "decreased"
            messages.append(
                f"Break time {direction} by {abs(break_pct):.0f}% "
                "compared to previous period."
            )

        if not messages:
            messages.append("Not enough data for comparison.")

        for msg in messages:
            label = QLabel(msg)
            label.setObjectName("subtitle")
            label.setWordWrap(True)
            self._comparison_layout.addWidget(label)

    def _show_placeholder_stats(self) -> None:
        """Show placeholder stats when no service is available."""
        while self._summary_container.count():
            item = self._summary_container.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        placeholders = [
            ("Focus Time", "--", "No data"),
            ("Break Time", "--", "No data"),
            ("Breaks Completed", "--", "No data"),
            ("Smart Monitoring", "--", "No data"),
            ("Estimated Blink Rate", "--", "No data"),
        ]
        for title, value, subtitle in placeholders:
            card = SummaryCard(title, value, subtitle)
            self._summary_container.addWidget(card)

    def _on_export(self) -> None:
        """Export all data as JSON."""
        import json

        from PySide6.QtWidgets import QFileDialog, QMessageBox

        if self.deps.analytics_service is None:
            QMessageBox.warning(
                self,
                "Export",
                "Analytics service not available.",
            )
            return

        data = self.deps.analytics_service.export_all_data()

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            f"eye_health_data_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json)",
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                QMessageBox.information(
                    self,
                    "Export Complete",
                    f"Data exported to:\n{file_path}\n\n"
                    f"Timer sessions: {len(data.get('timer_sessions', []))}\n"
                    f"Monitoring sessions: {len(data.get('monitoring_sessions', []))}\n"
                    f"Blink measurements: {len(data.get('blink_measurements', []))}",
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export data:\n{e}",
                )

    def _on_delete_all(self) -> None:
        """Delete all data with confirmation."""
        from PySide6.QtWidgets import QMessageBox

        if self.deps.analytics_service is None:
            return

        reply = QMessageBox.warning(
            self,
            "Delete All Data",
            "This will permanently delete:\n\n"
            "- All timer sessions\n"
            "- All monitoring sessions\n"
            "- All blink measurements\n"
            "- All statistics history\n\n"
            "This action cannot be undone.\n\n"
            "Are you sure you want to delete all data?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            count = self.deps.analytics_service.delete_all_data()
            QMessageBox.information(
                self,
                "Data Deleted",
                f"Successfully deleted {count} records.",
            )
            self._load_statistics()
