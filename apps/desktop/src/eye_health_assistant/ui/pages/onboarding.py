"""Onboarding wizard — first-launch experience."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from eye_health_assistant.app.dependencies import Dependencies


class _ClickableCard(QFrame):
    """A QFrame that emits clicked when pressed."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._radio: QRadioButton | None = None

    def set_radio(self, radio: QRadioButton) -> None:
        self._radio = radio

    def mousePressEvent(self, event: QMouseEvent | None) -> None:  # noqa: N802
        if self._radio is not None and event is not None:
            self._radio.setChecked(True)
        if event is not None:
            super().mousePressEvent(event)


class OnboardingPage(QWidget):
    """Multi-step onboarding wizard for first launch."""

    completed = Signal()

    def __init__(self, deps: Dependencies, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.deps = deps
        self._current_step = 0
        self._selected_mode = "timer"
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Content area with stacked pages
        self._stack = QStackedWidget()
        self._stack.addWidget(self._build_welcome_step())
        self._stack.addWidget(self._build_privacy_step())
        self._stack.addWidget(self._build_mode_step())
        self._stack.addWidget(self._build_theme_step())
        self._stack.addWidget(self._build_finish_step())
        layout.addWidget(self._stack, 1)

        # Navigation bar
        nav_bar = QFrame()
        nav_bar.setObjectName("card")
        nav_bar.setFrameShape(QFrame.Shape.NoFrame)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(24, 16, 24, 16)

        self._back_btn = QPushButton("Back")
        self._back_btn.setObjectName("secondary-button")
        self._back_btn.setAccessibleName("Go to previous step")
        self._back_btn.clicked.connect(self._go_back)
        self._back_btn.setVisible(False)
        nav_layout.addWidget(self._back_btn)

        nav_layout.addStretch()

        # Step indicator
        self._step_label = QLabel("Step 1 of 5")
        self._step_label.setObjectName("caption")
        nav_layout.addWidget(self._step_label)

        nav_layout.addStretch()

        self._next_btn = QPushButton("Next")
        self._next_btn.setAccessibleName("Go to next step")
        self._next_btn.clicked.connect(self._go_next)
        nav_layout.addWidget(self._next_btn)

        layout.addWidget(nav_bar)

    def _build_welcome_step(self) -> QWidget:
        """Step 1: Welcome."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 40)
        layout.setSpacing(24)

        title = QLabel("Welcome to Eye Health Assistant")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "A privacy-first desktop companion that helps you maintain "
            "healthier screen-use habits."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        features = [
            "Timer-based focus sessions with gentle reminders",
            "Optional camera-based blink monitoring (fully local)",
            "Guided eye exercises and educational content",
            "Statistics and history — all stored locally",
        ]
        for feature in features:
            feature_label = QLabel(f"  {feature}")
            feature_label.setObjectName("subtitle")
            feature_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(feature_label)

        layout.addStretch()
        return page

    def _build_privacy_step(self) -> QWidget:
        """Step 2: Privacy."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 40)
        layout.setSpacing(24)

        title = QLabel("Your Privacy Matters")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "Eye Health Assistant is built with privacy as a core principle."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        privacy_points = [
            "All data is stored locally on your device",
            "Camera processing happens entirely on your computer",
            "No webcam frames are ever recorded or uploaded",
            "No account or internet connection required",
            "You can delete all data at any time",
        ]
        for point in privacy_points:
            point_label = QLabel(f"  {point}")
            point_label.setObjectName("subtitle")
            point_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(point_label)

        layout.addStretch()
        return page

    def _build_mode_step(self) -> QWidget:
        """Step 3: Choose monitoring mode."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 40)
        layout.setSpacing(24)

        title = QLabel("Choose Your Mode")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "You can switch between modes at any time in Settings."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Mode selection
        self._mode_group = QButtonGroup(self)

        timer_option = self._build_mode_option(
            "Timer Mode",
            "No camera required. Configurable focus and break timers "
            "with gentle notifications.",
            "timer",
        )
        smart_option = self._build_mode_option(
            "Smart Mode",
            "Optional camera-based monitoring to estimate blink rate "
            "and detect prolonged screen use.",
            "smart",
        )

        self._mode_group.addButton(timer_option[0], 0)
        self._mode_group.addButton(smart_option[0], 1)

        layout.addWidget(timer_option[1])
        layout.addWidget(smart_option[1])

        # Default to timer mode
        timer_option[0].setChecked(True)

        layout.addStretch()
        return page

    def _build_mode_option(
        self, title: str, description: str, mode: str
    ) -> tuple[QRadioButton, _ClickableCard]:
        """Build a selectable mode option card."""
        card = _ClickableCard()
        card.setObjectName("card")
        card.setFrameShape(QFrame.Shape.NoFrame)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)
        card_layout.setSpacing(16)

        radio = QRadioButton()
        radio.setAccessibleName(f"Select {title}")
        card_layout.addWidget(radio)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName("section-title")
        text_layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setObjectName("subtitle")
        desc_label.setWordWrap(True)
        text_layout.addWidget(desc_label)

        card_layout.addLayout(text_layout, 1)

        # Store mode on the card for later retrieval
        card.setProperty("mode", mode)

        # Clicking the card selects the radio button
        card.set_radio(radio)

        return radio, card

    def _build_theme_step(self) -> QWidget:
        """Step 4: Choose theme."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 40)
        layout.setSpacing(24)

        title = QLabel("Choose Your Theme")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "Select a theme that's comfortable for your eyes. "
            "You can change this later."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        self._theme_group = QButtonGroup(self)

        dark_option = self._build_theme_option(
            "Dark", "Easier on the eyes in low light"
        )
        light_option = self._build_theme_option(
            "Light", "Clean and bright for well-lit environments"
        )
        system_option = self._build_theme_option(
            "System", "Match your operating system setting"
        )

        self._theme_group.addButton(dark_option[0], 0)
        self._theme_group.addButton(light_option[0], 1)
        self._theme_group.addButton(system_option[0], 2)

        layout.addWidget(dark_option[1])
        layout.addWidget(light_option[1])
        layout.addWidget(system_option[1])

        # Default to dark theme
        dark_option[0].setChecked(True)

        layout.addStretch()
        return page

    def _build_theme_option(
        self, title: str, description: str
    ) -> tuple[QRadioButton, _ClickableCard]:
        """Build a selectable theme option."""
        card = _ClickableCard()
        card.setObjectName("card")
        card.setFrameShape(QFrame.Shape.NoFrame)
        card.setCursor(Qt.CursorShape.PointingHandCursor)

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 12, 20, 12)
        card_layout.setSpacing(16)

        radio = QRadioButton()
        radio.setAccessibleName(f"Select {title} theme")
        card_layout.addWidget(radio)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setObjectName("section-title")
        text_layout.addWidget(title_label)

        desc_label = QLabel(description)
        desc_label.setObjectName("subtitle")
        text_layout.addWidget(desc_label)

        card_layout.addLayout(text_layout, 1)

        card.set_radio(radio)

        return radio, card

    def _build_finish_step(self) -> QWidget:
        """Step 5: Finish."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 40)
        layout.setSpacing(24)

        title = QLabel("You're All Set!")
        title.setObjectName("page-title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "Start focusing on your work with healthier habits.\n\n"
            "Remember: you can always adjust settings, switch modes, "
            "or take a break."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addStretch()

        self._finish_btn = QPushButton("Get Started")
        self._finish_btn.setAccessibleName(
            "Complete onboarding and start using the app"
        )
        self._finish_btn.clicked.connect(self._finish)
        finish_layout = QHBoxLayout()
        finish_layout.addStretch()
        finish_layout.addWidget(self._finish_btn)
        finish_layout.addStretch()
        layout.addLayout(finish_layout)

        layout.addStretch()
        return page

    def _go_next(self) -> None:
        """Advance to the next step."""
        if self._current_step < 4:
            self._current_step += 1
            self._stack.setCurrentIndex(self._current_step)
            self._update_nav()

    def _go_back(self) -> None:
        """Go to the previous step."""
        if self._current_step > 0:
            self._current_step -= 1
            self._stack.setCurrentIndex(self._current_step)
            self._update_nav()

    def _update_nav(self) -> None:
        """Update navigation buttons and step indicator."""
        self._back_btn.setVisible(self._current_step > 0)
        self._step_label.setText(f"Step {self._current_step + 1} of 5")

        if self._current_step == 4:
            self._next_btn.setVisible(False)
        else:
            self._next_btn.setVisible(True)

    def _finish(self) -> None:
        """Complete onboarding and apply selections."""
        # Apply theme selection
        theme_map = {0: "dark", 1: "light", 2: "system"}
        theme_id = self._theme_group.checkedId()
        self.deps.config.theme = theme_map.get(theme_id, "dark")

        # Apply mode selection
        self.deps.config.smart_mode_default = (
            self._mode_group.checkedId() == 1
        )

        # Mark onboarding as completed
        self.deps.config.onboarding_completed = True

        # Save config
        self.deps.save_config()

        self.completed.emit()
