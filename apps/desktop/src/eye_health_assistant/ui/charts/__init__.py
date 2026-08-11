"""Chart widgets for analytics visualization."""

from __future__ import annotations

import contextlib
from dataclasses import dataclass

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout, QWidget


@dataclass
class ChartDataPoint:
    """A single data point for a chart."""

    label: str
    value: float
    tooltip: str = ""


@dataclass
class ChartSeries:
    """A series of data points for a chart."""

    name: str
    points: list[ChartDataPoint]
    color: str = "#4A90D9"


class BarChartWidget(QFrame):
    """Simple bar chart widget using QPainter."""

    def __init__(
        self,
        title: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(200)
        self.setMinimumWidth(300)

        self._title = title
        self._series: ChartSeries | None = None
        self._max_value: float = 0.0
        self._bar_color = QColor("#4A90D9")
        self._grid_color = QColor("#3A3A3A")
        self._text_color = QColor("#CCCCCC")

    def set_data(self, series: ChartSeries) -> None:
        """Set the chart data."""
        self._series = series
        if series.points:
            self._max_value = max(p.value for p in series.points) * 1.2
            if self._max_value == 0:
                self._max_value = 1.0
            try:
                self._bar_color = QColor(series.color)
            except Exception:
                self._bar_color = QColor("#4A90D9")
        self.update()

    def set_colors(
        self,
        bar_color: str = "#4A90D9",
        grid_color: str = "#3A3A3A",
        text_color: str = "#CCCCCC",
    ) -> None:
        """Set chart colors."""
        with contextlib.suppress(Exception):
            self._bar_color = QColor(bar_color)
        with contextlib.suppress(Exception):
            self._grid_color = QColor(grid_color)
        with contextlib.suppress(Exception):
            self._text_color = QColor(text_color)
        self.update()

    def paintEvent(self, _event: object) -> None:  # noqa: N802
        """Render the chart."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        margin_top = 40
        margin_bottom = 40
        margin_left = 50
        margin_right = 20

        chart_rect = QRect(
            rect.left() + margin_left,
            rect.top() + margin_top,
            rect.width() - margin_left - margin_right,
            rect.height() - margin_top - margin_bottom,
        )

        # Draw title
        if self._title:
            painter.setPen(QPen(self._text_color))
            font = QFont("Helvetica", 12, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(
                QRect(rect.left() + 10, rect.top() + 5, rect.width() - 20, 30),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                self._title,
            )

        if not self._series or not self._series.points:
            painter.setPen(QPen(self._text_color))
            font = QFont("Helvetica", 10)
            painter.setFont(font)
            painter.drawText(
                chart_rect,
                Qt.AlignmentFlag.AlignCenter,
                "No data available",
            )
            painter.end()
            return

        points = self._series.points
        n = len(points)
        if n == 0:
            painter.end()
            return

        # Draw grid lines
        painter.setPen(QPen(self._grid_color, 1, Qt.PenStyle.DotLine))
        grid_lines = 4
        for i in range(grid_lines + 1):
            y = chart_rect.top() + int(
                chart_rect.height() * (1 - i / grid_lines)
            )
            painter.drawLine(chart_rect.left(), y, chart_rect.right(), y)

            # Draw y-axis labels
            value = self._max_value * (i / grid_lines)
            label = f"{value / 60:.0f}h" if value >= 60 else f"{value:.0f}"
            painter.setPen(QPen(self._text_color))
            font = QFont("Helvetica", 8)
            painter.setFont(font)
            painter.drawText(
                QRect(0, y - 10, margin_left - 5, 20),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                label,
            )
            painter.setPen(QPen(self._grid_color, 1, Qt.PenStyle.DotLine))

        # Draw bars
        bar_width = max(4, (chart_rect.width() - 20) // max(n, 1) - 8)
        total_bars_width = n * bar_width + (n - 1) * 8
        start_x = chart_rect.left() + (chart_rect.width() - total_bars_width) // 2

        for i, point in enumerate(points):
            x = start_x + i * (bar_width + 8)
            bar_height = int(chart_rect.height() * (point.value / self._max_value))
            y = chart_rect.top() + chart_rect.height() - bar_height

            # Draw bar
            painter.setBrush(QBrush(self._bar_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y, bar_width, bar_height, 3, 3)

            # Draw label
            painter.setPen(QPen(self._text_color))
            font = QFont("Helvetica", 7)
            painter.setFont(font)
            label_rect = QRect(
                x - 5,
                chart_rect.top() + chart_rect.height() + 5,
                bar_width + 10,
                25,
            )
            painter.drawText(
                label_rect,
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                point.label,
            )

            # Draw value on top of bar
            if point.value > 0:
                painter.setPen(QPen(self._text_color))
                font = QFont("Helvetica", 7)
                painter.setFont(font)
                value_rect = QRect(x - 5, y - 18, bar_width + 10, 15)
                painter.drawText(
                    value_rect,
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
                    f"{point.value:.1f}",
                )

        painter.end()


class LineChartWidget(QFrame):
    """Simple line chart widget using QPainter."""

    def __init__(
        self,
        title: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(200)
        self.setMinimumWidth(300)

        self._title = title
        self._series: list[ChartSeries] = []
        self._max_value: float = 0.0
        self._line_color = QColor("#4A90D9")
        self._grid_color = QColor("#3A3A3A")
        self._text_color = QColor("#CCCCCC")

    def set_data(self, series: list[ChartSeries]) -> None:
        """Set multiple data series."""
        self._series = series
        max_val = 0.0
        for s in series:
            for p in s.points:
                max_val = max(max_val, p.value)
        self._max_value = max_val * 1.2 if max_val > 0 else 1.0
        self.update()

    def set_colors(
        self,
        line_color: str = "#4A90D9",
        grid_color: str = "#3A3A3A",
        text_color: str = "#CCCCCC",
    ) -> None:
        """Set chart colors."""
        with contextlib.suppress(Exception):
            self._line_color = QColor(line_color)
        with contextlib.suppress(Exception):
            self._grid_color = QColor(grid_color)
        with contextlib.suppress(Exception):
            self._text_color = QColor(text_color)
        self.update()

    def paintEvent(self, _event: object) -> None:  # noqa: N802
        """Render the chart."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        margin_top = 40
        margin_bottom = 40
        margin_left = 50
        margin_right = 20

        chart_rect = QRect(
            rect.left() + margin_left,
            rect.top() + margin_top,
            rect.width() - margin_left - margin_right,
            rect.height() - margin_top - margin_bottom,
        )

        # Draw title
        if self._title:
            painter.setPen(QPen(self._text_color))
            font = QFont("Helvetica", 12, QFont.Weight.Bold)
            painter.setFont(font)
            painter.drawText(
                QRect(rect.left() + 10, rect.top() + 5, rect.width() - 20, 30),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                self._title,
            )

        if not self._series:
            painter.setPen(QPen(self._text_color))
            font = QFont("Helvetica", 10)
            painter.setFont(font)
            painter.drawText(
                chart_rect,
                Qt.AlignmentFlag.AlignCenter,
                "No data available",
            )
            painter.end()
            return

        # Draw grid lines
        painter.setPen(QPen(self._grid_color, 1, Qt.PenStyle.DotLine))
        grid_lines = 4
        for i in range(grid_lines + 1):
            y = chart_rect.top() + int(
                chart_rect.height() * (1 - i / grid_lines)
            )
            painter.drawLine(chart_rect.left(), y, chart_rect.right(), y)

            value = self._max_value * (i / grid_lines)
            painter.setPen(QPen(self._text_color))
            font = QFont("Helvetica", 8)
            painter.setFont(font)
            painter.drawText(
                QRect(0, y - 10, margin_left - 5, 20),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                f"{value:.1f}",
            )
            painter.setPen(QPen(self._grid_color, 1, Qt.PenStyle.DotLine))

        # Draw each series
        colors = ["#4A90D9", "#E8913A", "#4CAF50", "#E85D5D"]
        for si, series in enumerate(self._series):
            if not series.points:
                continue

            try:
                color = QColor(series.color)
            except Exception:
                color = QColor(colors[si % len(colors)])

            n = len(series.points)
            if n == 1:
                x = chart_rect.left() + chart_rect.width() // 2
                y_val = series.points[0].value
                y = chart_rect.top() + int(
                    chart_rect.height() * (1 - y_val / self._max_value)
                )
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(x - 4, y - 4, 8, 8)
                continue

            step_x = chart_rect.width() / max(n - 1, 1)

            # Draw line
            painter.setPen(QPen(color, 2))
            prev_x = chart_rect.left()
            prev_y = chart_rect.top() + int(
                chart_rect.height()
                * (1 - series.points[0].value / self._max_value)
            )

            for i in range(1, n):
                x = chart_rect.left() + int(i * step_x)
                y = chart_rect.top() + int(
                    chart_rect.height()
                    * (1 - series.points[i].value / self._max_value)
                )
                painter.drawLine(prev_x, prev_y, x, y)
                prev_x = x
                prev_y = y

            # Draw dots
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            for i, point in enumerate(series.points):
                x = chart_rect.left() + int(i * step_x)
                y = chart_rect.top() + int(
                    chart_rect.height() * (1 - point.value / self._max_value)
                )
                painter.drawEllipse(x - 3, y - 3, 6, 6)

            # Draw x-axis labels (first, middle, last)
            if n > 0:
                painter.setPen(QPen(self._text_color))
                font = QFont("Helvetica", 7)
                painter.setFont(font)

                indices = [0, n // 2, n - 1] if n > 2 else [0, n - 1]
                for idx in indices:
                    if 0 <= idx < n:
                        x = chart_rect.left() + int(idx * step_x)
                        label_rect = QRect(
                            x - 20,
                            chart_rect.top() + chart_rect.height() + 5,
                            40,
                            25,
                        )
                        painter.drawText(
                            label_rect,
                            Qt.AlignmentFlag.AlignHCenter
                            | Qt.AlignmentFlag.AlignTop,
                            series.points[idx].label,
                        )

        painter.end()


class SummaryCard(QFrame):
    """A summary metric card with value and optional trend."""

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str = "",
        trend: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("metric-card")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._title_label = QLabel(title)
        self._title_label.setObjectName("caption")
        layout.addWidget(self._title_label)

        self._value_label = QLabel(value)
        self._value_label.setObjectName("stat-number")
        layout.addWidget(self._value_label)

        self._subtitle_label = QLabel(subtitle) if subtitle else None
        if self._subtitle_label:
            self._subtitle_label.setObjectName("caption")
            layout.addWidget(self._subtitle_label)

        self._trend_label = QLabel(trend) if trend else None
        if self._trend_label:
            self._trend_label.setObjectName("caption")
            layout.addWidget(self._trend_label)

        layout.addStretch()

    def update_value(
        self,
        value: str,
        subtitle: str | None = None,
        trend: str | None = None,
    ) -> None:
        """Update displayed values."""
        self._value_label.setText(value)
        if subtitle is not None:
            if self._subtitle_label is None:
                self._subtitle_label = QLabel(subtitle)
                self._subtitle_label.setObjectName("caption")
                self.layout().insertWidget(2, self._subtitle_label)  # type: ignore
            else:
                self._subtitle_label.setText(subtitle)
        if trend is not None:
            if self._trend_label is None:
                self._trend_label = QLabel(trend)
                self._trend_label.setObjectName("caption")
                self.layout().addWidget(self._trend_label)  # type: ignore
            else:
                self._trend_label.setText(trend)
