# PRD.md — Eye Health Assistant

**Document status:** Production Blueprint / Single Source of Truth\
**Version:** 1.0.0\
**Last updated:** 2026-08-08\
**Primary platforms:** Windows 10/11 and macOS 13+\
**Repository model:** Monorepo\
**Desktop app:** Python + PySide6\
**Landing site:** Next.js + TypeScript\
**Local-first storage:** SQLite\
**Cloud dependency for core functionality:** None

---

## 1. Executive Summary

Eye Health Assistant is a privacy-first desktop application designed to help
people who spend long periods working at a computer maintain healthier
screen-use habits.

The product combines two monitoring modes:

1. **Smart Mode** — optional webcam-based observation of face/eye landmarks to
   estimate blink behavior and related screen-use signals.
2. **Privacy/Timer Mode** — no camera required; uses configurable timers and
   reminders.

The application is not a medical diagnostic device. It provides educational
information, wellness reminders, and screen-use observations. It must never
present a calculated score as a medical diagnosis.

The product consists of two applications inside one monorepo:

- `apps/desktop`: the complete Python desktop application.
- `apps/web`: a Next.js landing website that explains the product, privacy
  model, features, downloads, documentation links, and FAQs.

The desktop application is the core product. The website is informational and
must not become a dependency of the desktop app.

---

# 2. Product Vision

Create a polished, calm, privacy-first desktop companion that helps users notice
prolonged screen use and maintain healthier visual habits without making them
feel monitored or interrupted constantly.

The product should feel like a professional desktop utility rather than a
prototype.

### Product principles

- **Privacy first**
- **Local first**
- **Helpful, not annoying**
- **Evidence-aware**
- **Accessible**
- **Cross-platform**
- **Simple at first glance, powerful when explored**
- **No unnecessary cloud account**
- **No forced camera usage**
- **No medical diagnosis**
- **Data belongs to the user**

---

# 3. Goals

## 3.1 Primary goals

- Track desktop screen-use sessions.
- Provide optional webcam-based blink estimation.
- Provide a camera-free timer mode.
- Encourage regular visual breaks.
- Provide educational eye-care content.
- Provide guided exercises with clear instructions and optional animations.
- Store useful history locally.
- Provide meaningful statistics and trends.
- Support light and dark themes.
- Support Windows and macOS.
- Provide a clean, professional desktop UI.
- Make the product usable by non-developers through packaged installers.
- Keep the core product functional without an internet connection.

## 3.2 Secondary goals

- Provide configurable notification behavior.
- Provide focus sessions that avoid unnecessary interruptions.
- Provide an insights system based on locally collected data.
- Provide export/delete controls for user data.
- Provide a polished landing website.
- Make the codebase maintainable by multiple developers and AI coding agents.

## 3.3 Non-goals

The application must not:

- Diagnose dry eye disease.
- Diagnose computer vision syndrome.
- Diagnose any eye condition.
- Claim that a proprietary "eye fatigue score" is medically validated.
- Replace an optometrist or ophthalmologist.
- Store webcam video by default.
- Upload webcam frames to a server.
- Require a cloud account for normal desktop use.
- Build a social network.
- Collect advertising data.
- Use manipulative notification patterns.

---

# 4. Target Users

## 4.1 Primary user

A person who spends substantial time using:

- laptops
- desktop computers
- programming environments
- browsers
- documentation
- video content
- design software
- office applications

They want reminders and useful statistics but do not want intrusive software.

## 4.2 Privacy-conscious user

Does not want webcam monitoring.

They should be able to use the product entirely through timer-based monitoring.

## 4.3 Developer / power user

Wants:

- detailed statistics
- configurable thresholds
- focus sessions
- local data
- keyboard shortcuts
- technical controls

## 4.4 General user

Wants:

- simple reminders
- exercises
- easy-to-understand information
- minimal configuration

---

# 5. Product Scope

The desktop application contains these primary areas:

1. Dashboard
2. Live Monitoring
3. Timer / Privacy Mode
4. Exercises
5. Exercise Detail
6. Eye Care / Learning Center
7. Eye Care Detail
8. Statistics
9. History
10. Settings
11. Notifications / reminder system
12. Onboarding and permissions
13. System tray / menu-bar integration
14. Data management

The website contains:

1. Landing page
2. Product overview
3. Features
4. Privacy
5. How it works
6. Screenshots/product preview
7. Download section
8. FAQ
9. Documentation links
10. Roadmap
11. Contact/project information

---

# 6. Core Product Modes

## 6.1 Smart Mode

Smart Mode uses the user's webcam only when explicitly enabled.

Possible signals:

- face detected/not detected
- eye landmarks
- estimated eye openness
- blink events
- blink frequency
- continuous monitoring duration
- optional estimated face-to-screen distance

### Privacy requirements

- Camera permission must be explicitly requested.
- Camera must have an obvious enabled/disabled state.
- No webcam video should be persisted by default.
- No frames should be uploaded.
- Processing should happen locally.
- The user must be able to disable Smart Mode instantly.
- If the camera becomes unavailable, the application should gracefully fall back
  to timer mode.
- The UI must clearly communicate whether the camera is active.

### Important engineering rule

Blink detection is an estimate, not a clinical measurement.

The UI must use wording such as:

- "Estimated blink rate"
- "Estimated monitoring data"
- "Local camera processing"

and must avoid medical claims.

---

## 6.2 Privacy / Timer Mode

Timer Mode works without camera access.

Users can choose:

- 20-20-20 style reminders
- custom focus duration
- custom break duration
- reminder frequency
- notification style
- quiet hours

Example preset:

- Focus: 20 minutes
- Visual break: 20 seconds

Another configurable preset:

- Focus: 25 minutes
- Break: 5 minutes

The exact defaults must remain configurable.

---

# 7. Dashboard

The dashboard is the primary screen.

## 7.1 Dashboard goals

The dashboard should answer:

- How long have I been on screens today?
- What is my current session?
- What mode am I using?
- Is the camera active?
- What is my estimated blink rate?
- When is my next break?
- How many breaks have I completed?
- What should I do now?

## 7.2 Suggested layout

### Header

- Application logo/name
- Current date
- Current mode
- Settings shortcut
- System status

### Today's Overview cards

Cards:

1. Screen Time
2. Estimated Blink Rate
3. Breaks
4. Wellness/Monitoring Status

### Live Monitoring card

Smart Mode:

- Camera status
- Face detected status
- Blink rate
- Monitoring duration
- Start/Stop control

Timer Mode:

- Current focus duration
- Time remaining
- Next break
- Start/Pause/Skip control

### Current Session

Show:

- session start
- current duration
- current mode
- interruptions
- breaks

### Quick Actions

- Start Smart Mode
- Start Timer
- Exercises
- Eye Care
- Statistics

### Recent Activity

Show recent events:

- focus started
- break completed
- reminder shown
- exercise completed

### Tip of the Day

One short educational recommendation.

---

# 8. Live Monitoring Screen

This screen provides more detail than the dashboard.

## 8.1 Smart Mode

Display:

- camera state
- face detection state
- estimated blink rate
- blink count
- monitoring duration
- optional eye openness indicator
- optional screen-distance estimate
- current reminder state

Do not display alarming medical language.

## 8.2 Timer Mode

Display:

- large countdown
- focus/break state
- progress indicator
- pause
- resume
- skip
- end session

## 8.3 Camera preview

Camera preview should be optional.

Default behavior should favor privacy.

If preview is shown:

- clearly label it
- provide disable control
- never record it

---

# 9. Blink Detection

## 9.1 Technology

Preferred stack:

- OpenCV
- MediaPipe
- NumPy

## 9.2 Processing pipeline

1. Open webcam.
2. Capture frame.
3. Detect face landmarks.
4. Extract eye landmark coordinates.
5. Calculate eye aspect ratio or equivalent geometric openness metric.
6. Detect transition from open -> closed -> open.
7. Count a blink when conditions are satisfied.
8. Apply smoothing/debouncing.
9. Aggregate blink events over time.
10. Store only derived metrics required by the product.

## 9.3 Blink-rate calculation

Use a configurable rolling window.

Example:

```text
blink_rate = blinks_in_window / window_duration_minutes
```

Do not use a single-minute sample as the only signal.

Recommended approach:

- rolling 3-5 minute window
- minimum observation duration
- smoothing
- outlier rejection

## 9.4 Low-blink notification

Do not trigger a notification from one low sample.

A configurable rule should require sustained evidence, for example:

```text
IF monitoring is active
AND enough valid observations exist
AND rolling blink rate remains below configured threshold
FOR a sustained period
THEN suggest a blink/break
```

Thresholds must be configurable.

The app must phrase this as a wellness reminder, not a medical warning.

---

# 10. Eye Fatigue / Wellness Score

The product may provide a user-facing "Eye Comfort" or "Screen Wellness" score.

It must not be represented as a clinical score.

Possible inputs:

- continuous screen duration
- break adherence
- estimated blink behavior
- reminder frequency
- optional distance signal
- recent session duration

Example conceptual weighting:

- Blink behavior: 40%
- Continuous screen exposure: 30%
- Break adherence: 15%
- Optional distance signal: 15%

These values are product defaults, not medical standards.

The algorithm must be versioned.

Example:

```text
score_algorithm_version = "1.0"
```

This allows future algorithm changes without corrupting historical
interpretation.

---

# 11. Screen Time Tracking

The desktop application should track application usage sessions only to the
extent necessary to calculate screen-use duration.

Minimum required data:

- session start
- session end
- duration
- active/inactive state
- mode

Avoid collecting application titles or detailed activity unless explicitly added
later and explicitly consented to.

The product should prioritize aggregate screen time.

---

# 12. Exercises

The Exercises section provides short guided visual-rest activities.

Examples:

- gentle blinking
- relaxed blinking
- looking away from the screen
- distance viewing
- short visual-rest routine
- guided break

Exercises must be educational and non-medical.

## 12.1 Exercise card

Each card contains:

- title
- short description
- estimated duration
- difficulty
- category
- start button

## 12.2 Exercise detail

When a user taps an exercise:

- title
- purpose
- safety note where appropriate
- step-by-step instructions
- animation or visual guide
- progress indicator
- countdown
- pause
- finish

Example structure:

```text
Exercise
↓
Why it may help
↓
How to do it
↓
Animated instruction
↓
Start
↓
Countdown
↓
Complete
↓
Completion saved locally
```

---

# 13. Eye Care / Learning Center

The Eye Care section contains educational cards.

Potential categories:

- Screen habits
- Breaks
- Blinking
- Workspace setup
- Lighting
- Screen positioning
- Hydration/general wellness
- When to seek professional advice
- FAQ

Every article should clearly distinguish general educational information from
medical advice.

The content should be stored locally in a structured content format so it can be
updated without rewriting UI logic.

---

# 14. Eye Care Detail Screen

When a card is selected:

- article title
- short summary
- sections
- illustrations/animations where useful
- actionable steps
- related exercises
- "start exercise" button where applicable
- disclaimer

The design should feel like a clean mini learning experience.

---

# 15. Statistics

Statistics show historical trends.

## 15.1 Daily

- total screen time
- focus sessions
- average session duration
- estimated blink rate
- breaks completed
- breaks skipped
- exercises completed

## 15.2 Weekly

- total screen time
- daily averages
- blink-rate trend
- break adherence
- session distribution

## 15.3 Monthly

- total screen time
- average daily use
- longest sessions
- exercise completion
- reminder patterns

Charts must be readable and accessible.

---

# 16. History

History is an event/session timeline.

Examples:

```text
09:10 — Focus session started
09:35 — Break reminder
09:36 — Break completed
10:10 — Exercise completed
11:20 — Smart monitoring started
```

Users can filter:

- day
- week
- month
- event type

---

# 17. Insights

Insights convert raw history into understandable observations.

Examples:

- "Your longest screen sessions usually happen in the morning."
- "You completed more breaks this week than last week."
- "Your estimated blink rate decreased during longer sessions."

Insights must be descriptive, not diagnostic.

Avoid:

- "You have dry eye."
- "Your eyes are unhealthy."
- "You have a medical condition."

---

# 18. Notifications

Notifications should be:

- gentle
- configurable
- dismissible
- rate-limited

Notification types:

- blink reminder
- break reminder
- session reminder
- exercise suggestion
- daily summary

Settings:

- enable/disable
- notification intensity
- quiet hours
- minimum interval
- sound on/off

Do not spam users.

---

# 19. Onboarding

First launch:

1. Welcome
2. Explain privacy
3. Choose Smart Mode or Timer Mode
4. Camera permission if Smart Mode selected
5. Configure reminder defaults
6. Select theme
7. Finish

Camera access must never be mandatory.

---

# 20. Settings

Settings categories:

## General

- startup behavior
- language
- theme
- system tray behavior

## Monitoring

- Smart Mode
- Timer Mode
- thresholds
- rolling-window duration

## Camera

- camera selection
- permission status
- preview preference

## Notifications

- enable/disable
- quiet hours
- sound
- reminder frequency

## Privacy

- local data location
- export data
- delete data
- clear history
- camera processing explanation

## Appearance

- Light
- Dark
- System

## Advanced

- logging
- diagnostics
- experimental features

---

# 21. Design System

## 21.1 Visual direction

Use a premium, calm, monochrome-first desktop design.

Characteristics:

- clean
- minimal
- spacious
- modern
- professional
- low visual noise

Use neutral colors as the foundation.

Accent colors may be used sparingly for:

- success
- warning
- active state
- destructive action

Do not make the entire UI colorful.

## 21.2 Themes

Required:

- Light
- Dark
- System

The same design tokens must drive all themes.

## 21.3 Typography

Use a modern system-friendly sans-serif font.

Create tokens for:

- display
- heading
- body
- caption
- label
- numeric/statistic

## 21.4 Spacing

Use a consistent spacing scale.

Example:

```text
4
8
12
16
24
32
48
64
```

## 21.5 Components

Create reusable components:

- Button
- IconButton
- Card
- MetricCard
- Badge
- Toggle
- Slider
- ProgressBar
- ProgressRing
- Dialog
- Modal
- Toast
- Tooltip
- Sidebar
- TopBar
- NavigationItem
- Chart
- EmptyState
- LoadingState
- ErrorState
- ExerciseCard
- ArticleCard
- SessionCard

---

# 22. Accessibility

The desktop app must support:

- keyboard navigation
- visible focus state
- adequate contrast
- scalable text where feasible
- semantic labels
- screen-reader-friendly controls where supported
- non-color-only status communication
- reduced-motion preference where possible

Animations must not be required to understand an instruction.

---

# 23. Desktop Technology Stack

## Required

### Python

Use a currently supported Python version compatible with all selected
dependencies. Pin and document the supported version.

### GUI

**PySide6**

Use Qt widgets and Qt application architecture.

### Computer vision

**OpenCV**

For webcam capture and image processing.

### Face/eye landmarks

**MediaPipe**

For local landmark estimation.

### Numerical calculations

**NumPy**

For geometric calculations and signal processing.

### Database

**SQLite**

Local embedded database.

### ORM / database access

Prefer SQLAlchemy if the project benefits from an explicit ORM layer. Otherwise
use a clean repository layer over SQLite.

The final implementation must avoid mixing SQL directly throughout UI code.

### Packaging

**PyInstaller** or an equivalent mature Python application packager.

The final choice must be documented and validated on both supported operating
systems.

---

# 24. Web Technology Stack

The landing site uses:

- Next.js
- TypeScript
- React
- CSS architecture appropriate for the selected Next.js version
- accessible components
- responsive design

The website is informational.

It must not be required for:

- desktop startup
- camera tracking
- timer mode
- database operations
- exercises
- statistics

---

# 25. Monorepo Architecture

Recommended structure:

```text
eye-health-assistant/
├── apps/
│   ├── desktop/
│   │   ├── src/
│   │   │   └── eye_health_assistant/
│   │   │       ├── app/
│   │   │       ├── core/
│   │   │       ├── domain/
│   │   │       ├── application/
│   │   │       ├── infrastructure/
│   │   │       ├── ui/
│   │   │       ├── monitoring/
│   │   │       ├── camera/
│   │   │       ├── blink/
│   │   │       ├── timer/
│   │   │       ├── notifications/
│   │   │       ├── exercises/
│   │   │       ├── content/
│   │   │       ├── analytics/
│   │   │       ├── settings/
│   │   │       └── utils/
│   │   ├── tests/
│   │   │   ├── unit/
│   │   │   ├── integration/
│   │   │   └── e2e/
│   │   ├── resources/
│   │   ├── scripts/
│   │   ├── pyproject.toml
│   │   └── README.md
│   │
│   └── web/
│       ├── app/
│       ├── components/
│       ├── content/
│       ├── lib/
│       ├── public/
│       ├── styles/
│       ├── tests/
│       ├── package.json
│       └── README.md
│
├── packages/
│   ├── config/
│   ├── docs/
│   └── design-tokens/
│
├── docs/
│   ├── architecture/
│   ├── adr/
│   ├── product/
│   ├── development/
│   ├── testing/
│   ├── release/
│   └── privacy/
│
├── scripts/
├── .github/
│   └── workflows/
├── PRD.md
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
└── Makefile
```

The AI implementation must preserve separation of concerns.

---

# 26. Python Internal Architecture

Use a layered architecture.

```text
UI
↓
Application Services
↓
Domain
↓
Infrastructure
```

## UI

Contains:

- windows
- pages
- reusable widgets
- dialogs
- theme system
- navigation

UI code must not contain database queries or computer-vision algorithms.

## Application layer

Coordinates use cases:

- start monitoring
- stop monitoring
- start timer
- finish break
- record blink event
- generate statistics
- complete exercise

## Domain

Contains business concepts:

- UserSettings
- MonitoringSession
- BlinkSample
- BreakSession
- Exercise
- ExerciseCompletion
- Reminder
- Insight
- DailyStatistics

## Infrastructure

Contains:

- SQLite repositories
- camera adapters
- MediaPipe adapters
- OS notification adapters
- filesystem storage
- logging

---

# 27. Recommended Python Package Structure

```text
eye_health_assistant/
├── __init__.py
├── main.py
├── app/
│   ├── __init__.py
│   ├── bootstrap.py
│   ├── dependencies.py
│   └── lifecycle.py
├── core/
│   ├── config.py
│   ├── constants.py
│   ├── logging.py
│   ├── exceptions.py
│   └── result.py
├── domain/
│   ├── models/
│   ├── enums/
│   ├── services/
│   └── value_objects/
├── application/
│   ├── services/
│   ├── commands/
│   ├── queries/
│   └── dto/
├── infrastructure/
│   ├── database/
│   ├── camera/
│   ├── computer_vision/
│   ├── notifications/
│   ├── filesystem/
│   └── platform/
├── monitoring/
│   ├── engine.py
│   ├── session_manager.py
│   └── metrics.py
├── blink/
│   ├── detector.py
│   ├── calculator.py
│   ├── smoothing.py
│   └── models.py
├── timer/
│   ├── engine.py
│   ├── presets.py
│   └── scheduler.py
├── analytics/
│   ├── statistics.py
│   ├── insights.py
│   └── scoring.py
├── exercises/
│   ├── catalog.py
│   ├── service.py
│   └── models.py
├── content/
│   ├── loader.py
│   └── schemas.py
├── settings/
│   ├── service.py
│   └── models.py
├── notifications/
│   ├── service.py
│   └── policies.py
└── ui/
    ├── main_window.py
    ├── navigation/
    ├── pages/
    ├── widgets/
    ├── dialogs/
    ├── themes/
    ├── animations/
    └── resources/
```

---

# 28. Database Design

SQLite is the source of truth for local application history.

Potential tables:

## settings

```text
id
key
value
value_type
updated_at
```

## monitoring_sessions

```text
id
mode
started_at
ended_at
duration_seconds
created_at
```

## blink_measurements

```text
id
session_id
window_start
window_end
blink_count
estimated_blink_rate
valid_observation_seconds
algorithm_version
created_at
```

## break_sessions

```text
id
session_id
started_at
ended_at
planned_duration_seconds
actual_duration_seconds
status
```

## reminders

```text
id
type
shown_at
action
source
```

## exercises

```text
id
slug
title
description
duration_seconds
difficulty
category
content_version
```

## exercise_completions

```text
id
exercise_id
started_at
completed_at
duration_seconds
```

## insights

```text
id
date
type
message
algorithm_version
```

## daily_statistics

```text
id
date
screen_time_seconds
focus_time_seconds
break_time_seconds
breaks_completed
breaks_skipped
estimated_average_blink_rate
exercise_count
score
algorithm_version
```

Use foreign keys and indexes appropriately.

---

# 29. Data Retention

Default retention should be reasonable and configurable.

The user must be able to:

- view stored data
- export data
- delete history
- delete all application data

Camera frames must not be retained by default.

---

# 30. Privacy

Privacy is a core product feature.

Requirements:

- no account required
- no cloud storage for core data
- no webcam uploads
- no default video recording
- local SQLite
- transparent permissions
- clear camera status
- export/delete controls
- privacy documentation
- minimal telemetry, preferably none by default

If future telemetry is ever introduced, it must be explicit, opt-in, documented,
and independent of core functionality.

---

# 31. Security

Implement:

- secure local file permissions where practical
- safe database handling
- input validation
- dependency pinning
- secret scanning
- dependency vulnerability scanning
- secure update process
- signed releases where feasible

Never store:

- passwords
- API keys
- authentication secrets

because the core app should not require them.

---

# 32. Error Handling

The application must gracefully handle:

- camera unavailable
- camera permission denied
- MediaPipe initialization failure
- invalid camera frame
- database unavailable
- corrupted database
- notification failure
- unsupported platform capability
- missing content
- packaging/resource path errors

The app should not crash because a camera is unavailable.

---

# 33. Logging

Use structured application logging.

Levels:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

Do not log:

- camera frames
- sensitive personal data
- unnecessary user activity

Provide a way to collect diagnostic logs without exposing private data.

---

# 34. Testing Strategy

Testing is mandatory.

## Unit tests

Test:

- blink calculations
- rolling windows
- threshold logic
- timer calculations
- statistics
- scoring
- repositories
- settings
- content validation

## Integration tests

Test:

- SQLite repositories
- monitoring service + repository
- timer + notification service
- exercise completion flow
- application service + infrastructure

## UI tests

Test:

- navigation
- theme switching
- dialogs
- settings
- exercise flow
- timer flow

## End-to-end tests

Critical paths:

1. first launch
2. onboarding
3. timer session
4. Smart Mode startup
5. camera permission denied
6. blink detection mock flow
7. break reminder
8. exercise completion
9. statistics generation
10. data export/delete

## Platform testing

Every release candidate must be tested on:

- supported Windows version(s)
- supported macOS version(s)

---

# 35. Computer Vision Testing

Never make tests depend on a physical camera.

Create mock/test adapters.

Test scenarios:

- face detected
- no face
- eyes open
- eyes closed
- blink
- multiple blinks
- false blink
- temporary tracking loss
- lighting change
- camera disconnect

Use deterministic fixtures.

---

# 36. Web Testing

Test:

- responsive layouts
- accessibility
- navigation
- download links
- FAQ
- privacy page
- dark/light theme if implemented
- SEO metadata
- broken links

Use modern TypeScript/React testing practices.

---

# 37. CI/CD

GitHub Actions should run:

### Python pipeline

- formatting
- linting
- type checking
- unit tests
- integration tests
- build validation

### Web pipeline

- install
- lint
- typecheck
- tests
- build

### Security

- dependency audit
- secret scanning

### Release

Produce platform-specific artifacts.

Do not assume a Windows artifact can be reliably built on macOS or vice versa
unless the build toolchain explicitly supports it.

Prefer native CI runners for final packaging.

---

# 38. Python Quality Tools

Use a modern Python toolchain.

Recommended:

- Ruff
- mypy or another strict type checker
- pytest
- pytest-qt where appropriate
- coverage
- pre-commit

The final tool choices must be documented in `CONTRIBUTING.md`.

---

# 39. Web Quality Tools

Recommended:

- ESLint
- TypeScript strict mode
- Prettier
- Playwright
- Vitest/Jest where appropriate

---

# 40. Documentation Deliverables

The project must contain:

## Root

- `README.md`
- `PRD.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `LICENSE`

## Documentation

- architecture
- development setup
- testing
- release
- privacy
- troubleshooting
- database
- UI/design system
- ADRs

---

# 41. README.md Requirements

The generated README must explain:

1. What the project is.
2. Features.
3. Privacy model.
4. Supported platforms.
5. Prerequisites.
6. Repository structure.
7. Development setup.
8. Python installation.
9. Node.js installation.
10. Package installation.
11. Running the desktop app.
12. Running the web app.
13. Running tests.
14. Formatting/linting.
15. Building desktop packages.
16. Building the website.
17. Environment variables, if any.
18. Troubleshooting.
19. Contribution.
20. License.

Example command sections should be kept accurate to the actual project scripts.

---

# 42. PREREQUISITES.md

Create a prerequisite document describing:

- supported Python version
- supported Node.js version
- package manager
- Git
- OS versions
- camera requirements for Smart Mode
- optional developer tools
- build requirements
- platform-specific dependencies

Do not document a version unless it has been tested.

---

# 43. DEVELOPMENT.md

Explain:

- repository setup
- dependency installation
- development commands
- architecture
- adding a new page
- adding a database model
- adding an exercise
- adding an eye-care article
- adding a notification
- adding a new computer-vision metric
- writing tests
- running quality checks

---

# 44. RELEASE.md

Explain:

- versioning
- changelog
- release branches/tags
- Windows build
- macOS build
- artifact naming
- signing/notarization where applicable
- release verification
- smoke tests
- rollback strategy

---

# 45. AI Coding Agent Rules

The project will be developed with AI coding tools.

AI agents must:

1. Read `PRD.md` before changing architecture.
2. Treat `PRD.md` as the product source of truth.
3. Never invent undocumented product requirements when an existing requirement
   is available.
4. Preserve the monorepo structure.
5. Keep UI, domain, application, and infrastructure layers separated.
6. Avoid putting business logic in UI widgets.
7. Avoid database queries inside UI code.
8. Write tests for new business logic.
9. Update documentation when behavior changes.
10. Keep cross-platform behavior in mind.
11. Never add cloud storage for local data without explicit approval.
12. Never persist webcam frames unless explicitly approved.
13. Never silently request camera permissions.
14. Never make medical claims.
15. Use type hints in Python.
16. Keep functions focused.
17. Prefer composition over unnecessary inheritance.
18. Avoid premature abstractions.
19. Avoid dead code.
20. Run relevant tests before declaring work complete.

---

# 46. AI Implementation Workflow

AI coding agents should work in phases.

## Phase 0 — Planning

- inspect repository
- read PRD
- identify dependencies
- confirm platform targets
- propose implementation plan

Do not immediately generate the entire application.

## Phase 1 — Foundation

Build:

- monorepo
- Python project
- PySide6 shell
- Next.js site
- shared documentation
- CI
- linting
- testing
- packaging skeleton

## Phase 2 — Desktop UI

Build:

- navigation
- theme system
- dashboard
- settings
- reusable components

## Phase 3 — Timer Mode

Build:

- timer engine
- presets
- break flow
- notifications
- history

## Phase 4 — Camera Mode

Build:

- camera permissions
- OpenCV adapter
- MediaPipe adapter
- blink detection
- monitoring service
- privacy controls

## Phase 5 — Exercises and Learning

Build:

- exercise catalog
- exercise detail
- animations
- Eye Care center
- article detail

## Phase 6 — Analytics

Build:

- statistics
- charts
- insights
- score calculation
- historical views

## Phase 7 — Hardening

Build:

- error handling
- accessibility
- performance improvements
- database migrations
- privacy review
- security review

## Phase 8 — Packaging

Build:

- Windows installer
- macOS application package
- release workflow
- documentation
- smoke tests

## Phase 9 — Website

Build:

- landing page
- features
- privacy
- FAQ
- downloads
- documentation
- responsive UI

---

# 47. Definition of Done

A feature is not complete until:

- implementation is complete
- UI is polished
- light theme works
- dark theme works
- keyboard navigation works where applicable
- error states exist
- loading states exist where applicable
- empty states exist
- tests exist
- documentation is updated
- no obvious platform-specific regression exists
- privacy implications are reviewed
- accessibility is considered

---

# 48. Performance Requirements

The app should remain lightweight during normal use.

Computer-vision processing must:

- avoid unnecessary frame processing
- use configurable sampling
- release camera resources correctly
- avoid memory leaks
- avoid blocking the UI thread

Long-running operations must not freeze the UI.

Use worker threads/processes where appropriate.

---

# 49. Threading / Concurrency

Never perform continuous camera processing on the Qt UI thread.

Recommended:

```text
UI Thread
   |
   +---- Monitoring Worker
            |
            +---- Camera
            +---- Landmark Detection
            +---- Blink Detection
            +---- Metrics
```

Results should be emitted safely back to the UI.

Database writes should also avoid blocking the UI.

---

# 50. Cross-Platform Requirements

The application must support:

## Windows

- installation
- startup
- camera permissions
- notifications
- system tray
- database paths
- packaging

## macOS

- application bundle
- camera permission behavior
- menu-bar/tray behavior
- notifications
- database paths
- packaging
- signing/notarization considerations

Platform-specific functionality must be isolated behind adapters.

---

# 51. Local File Layout

Use OS-appropriate application-data directories.

Do not hardcode:

```text
C:\...
```

or:

```text
/Users/...
```

Use platform-aware path resolution.

Example conceptual structure:

```text
App Data/
├── database/
│   └── app.sqlite
├── logs/
├── exports/
├── cache/
└── settings/
```

---

# 52. Data Export

Allow users to export their local history.

Recommended formats:

- JSON
- CSV

The export must include:

- session data
- statistics
- break records
- exercise completions
- derived blink metrics

Do not export raw camera frames because they should not exist.

---

# 53. Data Deletion

Provide:

- delete selected history
- delete date range
- delete all history
- reset application

Require confirmation for destructive operations.

---

# 54. Content Architecture

Exercise and eye-care content should be data-driven.

Example:

```text
content/
├── exercises/
│   ├── blinking.json
│   ├── visual_break.json
│   └── distance_viewing.json
└── eye_care/
    ├── screen_habits.json
    ├── workspace.json
    └── breaks.json
```

Validate content schemas at startup/build time.

---

# 55. Notification Policy

The notification engine should use a policy layer.

Inputs:

- current session
- last notification
- current mode
- quiet hours
- user preferences
- current reminder state

Outputs:

- no notification
- blink reminder
- break reminder
- exercise suggestion

Rate limit reminders to avoid annoyance.

---

# 56. System Tray / Menu Bar

The desktop application should support background operation.

Tray/menu-bar actions:

- Show Dashboard
- Start Timer
- Start Smart Mode
- Pause Monitoring
- Start Break
- Open Exercises
- Quit

The user must be able to understand whether monitoring is active.

---

# 57. Startup Behavior

Settings:

- start on login
- start minimized
- start monitoring automatically
- default mode

Defaults should favor privacy and user control.

---

# 58. UI States

Every major screen should define:

- loading
- normal
- empty
- error
- disabled
- permission denied
- offline/local state
- active monitoring
- paused state

---

# 59. Design Details for Key Screens

## Dashboard

Hierarchy:

```text
App Shell
 ├── Navigation
 └── Main Content
      ├── Header
      ├── Overview Metrics
      ├── Monitoring
      ├── Session
      ├── Quick Actions
      └── Recent Activity
```

## Exercises

```text
Header
Category filters
Exercise grid/list
Exercise cards
```

## Exercise Detail

```text
Back
Title
Summary
Visual/animation
Steps
Start button
Progress
Completion
```

## Eye Care

```text
Header
Categories
Educational cards
```

## Eye Care Detail

```text
Title
Summary
Content sections
Illustration
Action steps
Related exercise
```

## Statistics

```text
Time-range selector
Summary metrics
Charts
Trends
Insights
```

## History

```text
Filters
Timeline
Event cards
```

## Settings

```text
Sidebar categories
Settings panels
Save/apply behavior
```

---

# 60. Product Metrics

The app can measure product usage locally.

Potential metrics:

- sessions completed
- breaks completed
- break adherence
- exercises completed
- average session duration
- active days
- Smart Mode usage
- Timer Mode usage

These are local product statistics, not advertising analytics.

---

# 61. Success Criteria

The product is successful if a user can:

1. Install it without Python.
2. Launch it.
3. Understand what it does within one minute.
4. Choose camera or no-camera mode.
5. Start monitoring.
6. Receive useful reminders.
7. Complete an exercise.
8. Review history.
9. Understand weekly statistics.
10. Change themes.
11. Delete their data.
12. Use the app offline.
13. Run it on Windows and macOS.

---

# 62. Website Requirements

The Next.js site should communicate:

### Hero

- product name
- concise value proposition
- primary download CTA
- privacy-first message

### Features

- Smart Mode
- Timer Mode
- Exercises
- Statistics
- Local-first privacy
- Cross-platform

### How It Works

1. Choose mode.
2. Work normally.
3. Receive gentle reminders.
4. Take breaks.
5. Review trends.

### Privacy

Explain:

- local processing
- camera behavior
- no default recording
- local history
- no account required

### Downloads

Provide Windows and macOS downloads when releases exist.

### FAQ

Include:

- Does it require a camera?
- Does it upload video?
- Does it work offline?
- What is blink detection?
- Is it medical software?
- What operating systems are supported?

---

# 63. SEO and Website Quality

Next.js website should include:

- title metadata
- description
- Open Graph metadata
- sitemap
- robots configuration
- semantic HTML
- accessible headings
- optimized images
- responsive layout

---

# 64. Versioning

Use Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.0.0
```

Algorithm changes should be independently versioned where historical statistics
depend on them.

---

# 65. Database Migration Strategy

Database schema changes must use migrations.

Never modify production schema manually without a migration.

Migration requirements:

- deterministic
- versioned
- reversible where practical
- tested

---

# 66. Configuration

Configuration should have clear precedence:

```text
Defaults
↓
Config file
↓
User settings
```

Secrets must never be stored in source control.

The desktop app should work without environment variables for normal users.

---

# 67. Packaging for Non-Developers

Non-developers must not need:

- Python
- Node.js
- Git
- terminal
- package managers

The release artifact should include everything required to run the desktop app.

Developer setup and end-user installation must be separate.

---

# 68. Build Artifacts

Suggested names:

```text
EyeHealthAssistant-Windows-x64-v1.0.0.exe
EyeHealthAssistant-macOS-arm64-v1.0.0.dmg
EyeHealthAssistant-macOS-x64-v1.0.0.dmg
```

Actual artifact naming should be finalized according to the packaging system.

---

# 69. Troubleshooting Documentation

Document solutions for:

- camera permission denied
- camera not detected
- black camera preview
- notification not appearing
- app not starting
- database reset
- macOS permissions
- Windows security warnings
- broken update
- corrupted local data

---

# 70. Future Enhancements

Potential future features:

- additional platforms
- richer analytics
- optional wearable integrations
- advanced posture estimation
- improved computer-vision models
- optional synchronization
- accessibility improvements
- localization
- configurable dashboards

Future ideas must not complicate the initial product unnecessarily.

---

# 71. Explicit Product Constraints

These are mandatory unless the PRD is intentionally revised:

1. Python desktop application.
2. PySide6 GUI.
3. OpenCV for camera processing.
4. MediaPipe for eye/face landmarks.
5. NumPy for calculations.
6. SQLite local database.
7. Next.js landing website.
8. Monorepo.
9. Windows support.
10. macOS support.
11. Light and dark themes.
12. Camera mode is optional.
13. Timer mode works without camera.
14. Core functionality works offline.
15. No raw webcam video storage by default.
16. User-controlled local history.
17. Exercises and educational content.
18. Statistics and history.
19. Production-grade documentation.
20. Testing and CI.
21. Packaged builds for non-developers.

---

# 72. Final AI Agent Instruction

When implementing this project from this PRD:

**Do not attempt to implement the entire product in one uncontrolled
generation.**

Instead:

1. Read this document.
2. Inspect the repository.
3. Create an implementation plan.
4. Create the monorepo foundation.
5. Implement one phase at a time.
6. Run tests after each meaningful change.
7. Update documentation.
8. Keep architecture consistent.
9. Ask for clarification only when the requirement genuinely conflicts with this
   PRD.
10. Never silently replace a required technology.
11. Never add cloud infrastructure to the core desktop product.
12. Never weaken privacy requirements for convenience.
13. Never make medical claims.
14. Never consider a feature complete without tests and documentation.

---

# 73. Initial Implementation Order

The recommended first implementation sequence is:

```text
1. Repository + monorepo
2. Python packaging
3. PySide6 application shell
4. Theme/design system
5. Navigation
6. Dashboard UI
7. SQLite layer
8. Timer mode
9. Notification system
10. History
11. Exercises
12. Eye Care content
13. Statistics
14. Smart Mode
15. Blink detection
16. Insights
17. Data export/delete
18. Settings hardening
19. Cross-platform packaging
20. Next.js landing site
21. CI/CD
22. Release documentation
```

---

# 74. Final Definition of Product Readiness

The project can be considered production-ready only when:

- Windows build is installable and tested.
- macOS build is installable and tested.
- Core functionality works offline.
- Timer Mode works without camera.
- Smart Mode handles camera permission safely.
- Camera processing is local.
- Raw video is not persisted by default.
- Dashboard is polished.
- Light and dark themes work.
- Exercises work.
- Eye Care content works.
- Statistics work.
- History works.
- Data export/delete works.
- Notifications work.
- Settings work.
- Accessibility has been reviewed.
- Automated tests pass.
- CI passes.
- Documentation is complete.
- Release artifacts are reproducible.
- Privacy documentation is complete.
- No known critical security issue remains.
- No medical/diagnostic claims are presented.

---

# 75. Important Product Disclaimer

The application is a wellness and educational tool. It is not intended to
diagnose, treat, cure, or prevent disease.

If a user experiences persistent, severe, painful, or concerning eye symptoms,
the application should encourage them to seek advice from a qualified eye-care
professional rather than relying on application scores or reminders.

---

# 76. End of PRD

This document is the primary product and implementation reference for Eye Health
Assistant.

Any significant architectural or product decision that changes this
specification should be recorded in an Architecture Decision Record under:

```text
docs/adr/
```

and reflected back into this PRD when appropriate.
