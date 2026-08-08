# Eye Health Assistant — Desktop Application

A privacy-first desktop application that helps people who spend long periods working at a computer maintain healthier screen-use habits.

> **Disclaimer:** This is a wellness and educational tool. It is not intended to diagnose, treat, cure, or prevent disease.

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.12+ |
| GUI Framework | PySide6 (Qt) | 6.6+ |
| Camera Processing | OpenCV | Optional `[camera]` extra |
| Face/Eye Landmarks | MediaPipe | Optional `[camera]` extra |
| Numerical | NumPy | 1.24+ |
| Database | SQLite via SQLAlchemy | Local only |
| Linter | Ruff | Latest |
| Type Checker | mypy | Latest |
| Tests | pytest | Latest |
| Packaging | PyInstaller | Latest |

## Folder Structure

```
apps/desktop/
├── src/eye_health_assistant/        # Main package
│   ├── __init__.py                  # Package metadata
│   ├── __main__.py                  # Module runner (python -m eye_health_assistant)
│   ├── main.py                      # Application entry point
│   ├── app/                         # Bootstrap, lifecycle, dependencies
│   │   ├── lifecycle.py             # App init/shutdown
│   │   └── dependencies.py          # Dependency injection
│   ├── core/                        # Config, constants, exceptions, logging
│   │   ├── config.py                # App configuration
│   │   ├── constants.py             # Global constants
│   │   ├── exceptions.py            # Custom exceptions
│   │   ├── logging.py               # Structured logging
│   │   └── result.py                # Result type (Ok/Err)
│   ├── domain/                      # Models, enums, value objects
│   │   ├── enums/
│   │   ├── models/
│   │   ├── services/
│   │   └── value_objects/
│   ├── application/                 # Use cases, commands, queries, DTOs
│   │   ├── commands/
│   │   ├── dto/
│   │   ├── queries/
│   │   └── services/
│   ├── infrastructure/              # Database, camera, notifications
│   │   ├── camera/
│   │   ├── computer_vision/
│   │   ├── database/
│   │   ├── filesystem/
│   │   ├── notifications/
│   │   └── platform/
│   ├── monitoring/                  # Monitoring engine
│   ├── blink/                       # Blink detection
│   ├── timer/                       # Timer engine
│   ├── analytics/                   # Statistics, insights, scoring
│   ├── exercises/                   # Exercise catalog
│   ├── content/                     # Educational content loader
│   ├── settings/                    # Settings management
│   ├── notifications/               # Notification service
│   └── ui/                          # PySide6 UI layer
│       ├── main_window.py           # Main window with sidebar navigation
│       ├── pages/                   # Page widgets (dashboard, etc.)
│       ├── widgets/                 # Reusable widgets
│       ├── dialogs/                 # Modal dialogs
│       ├── themes/                  # Theme system (light/dark/system)
│       └── animations/              # UI animations
├── tests/
│   ├── unit/                        # Unit tests
│   └── integration/                 # Integration tests
├── resources/                       # Icons, images, stylesheets
├── pyproject.toml                   # Project config, dependencies, tool settings
├── .env                             # Environment variables (gitignored)
└── .env.example                     # Environment variable template
```

## Architecture

The desktop app follows a **layered architecture**:

```
UI  →  Application  →  Domain  →  Infrastructure
```

| Layer | Contains | Must NOT contain |
|-------|----------|-----------------|
| UI | Windows, pages, widgets, themes | Database queries, CV algorithms, business logic |
| Application | Use cases, commands, queries, DTOs | UI widgets, infrastructure details |
| Domain | Models, enums, value objects, services | UI code, infrastructure code |
| Infrastructure | SQLite repos, camera adapters, notifications | Business logic |

## Prerequisites

- Python 3.12+ (3.14 recommended)
- pip (comes with Python)
- Git

Optional:
- Camera — Required only for Smart Mode testing

## Quick Start

### 1. Clone and Install

```bash
cd apps/desktop
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

For camera support (Smart Mode):

```bash
pip install -e ".[camera]"
```

Or from the project root:

```bash
make install-desktop
```

### 2. Run the App

```bash
# Using Makefile (from project root)
make run-desktop

# Or manually
cd apps/desktop
source .venv/bin/activate
python -m eye_health_assistant
```

Press `Ctrl+C` to stop. The app handles SIGINT gracefully.

### 3. Environment Variables

Copy the example and adjust as needed:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `EYE_HEALTH_LOG_LEVEL` | Logging level | `INFO` |
| `EYE_HEALTH_THEME` | UI theme (light/dark/system) | `system` |
| `EYE_HEALTH_CAMERA_INDEX` | Camera device index | `0` |

No API keys or secrets are required.

## Development Commands

| Command | Description |
|---------|-------------|
| `python -m eye_health_assistant` | Run the app |
| `ruff check .` | Lint with Ruff |
| `ruff format .` | Format with Ruff |
| `mypy src/` | Type check with mypy |
| `pytest` | Run all tests |
| `pytest -v` | Verbose test output |
| `pytest tests/unit/` | Unit tests only |
| `pytest --cov=eye_health_assistant` | Coverage report |

### From Project Root

| Command | Description |
|---------|-------------|
| `make run-desktop` | Run the desktop app |
| `make test-desktop` | Run pytest |
| `make lint-python` | Run ruff + mypy |
| `make format-python` | Format Python code |
| `make check` | Full quality check (lint + test) |

## Testing

```bash
cd apps/desktop
source .venv/bin/activate

# Run all tests
pytest

# Verbose
pytest -v

# Unit tests only
pytest tests/unit/

# With coverage
pytest --cov=eye_health_assistant --cov-report=html
```

- Test business logic in isolation
- Use mocks for camera and platform code
- Never depend on a physical camera in tests
- Use deterministic fixtures

## Quality Checks

Before declaring any change complete, run:

```bash
# From project root
make check

# Or individually
cd apps/desktop
ruff check src/
mypy src/
pytest
```

All three must pass.

## Building for Production

### macOS

```bash
cd apps/desktop
source .venv/bin/activate
python -m PyInstaller --windowed --name EyeHealthAssistant main.py
```

Produces: `EyeHealthAssistant-macOS-arm64-v1.0.0.dmg`

### Windows

Must run on a Windows machine or CI runner:

```bash
python -m PyInstaller --windowed --name EyeHealthAssistant main.py
```

Produces: `EyeHealthAssistant-Windows-x64-v1.0.0.exe`

## Styling Rules (Critical)

These rules prevent UI bugs. Follow them exactly:

1. **No borders on global QWidget rule.** Only set `background-color`, `color`, `font-family`, `font-size`. Never put `border` on `QWidget {{ }}`.

2. **Labels inside cards must be explicitly borderless.** Always add:
   ```css
   #card QLabel, #metric-card QLabel {
       background-color: transparent;
       border: none;
   }
   ```

3. **All QFrame instances must call `setFrameShape(QFrame.Shape.NoFrame)`** in the constructor.

4. **Font family: Qt-compatible only.** Use `Helvetica, Arial, sans-serif`. Never use `-apple-system` or `SF Pro Text`.

5. **Card layouts: `setContentsMargins(0, 0, 0, 0)`** — padding comes from stylesheet only.

## Privacy Rules (Non-Negotiable)

1. Never persist webcam frames
2. Never upload camera data
3. Never make medical or diagnostic claims
4. Camera permission must be explicit
5. User data stays local
6. Camera status always visible in UI when active

## License

MIT License. See [LICENSE](../../LICENSE).
