# Eye Health Assistant

A privacy-first desktop application designed to help people who spend long
periods working at a computer maintain healthier screen-use habits.

> **Disclaimer:** This application is a wellness and educational tool. It is not
> intended to diagnose, treat, cure, or prevent disease.

## Features

- **Smart Mode** — Optional webcam-based estimation of blink behavior and
  screen-use signals (processed entirely on your device)
- **Timer Mode** — Camera-free configurable focus/break reminders
  (20-20-20 style or custom durations)
- **Exercises** — Short guided visual-rest activities with step-by-step
  instructions
- **Eye Care Center** — Educational content about healthy screen habits,
  workspace setup, lighting, and more
- **Statistics** — Historical trends and insights (daily, weekly, monthly)
- **History** — Event timeline with filtering by day, week, month, and event type
- **Insights** — Descriptive observations derived from your local data
- **Light & Dark Themes** — Comfortable viewing in any environment
- **System Tray** — Background operation with menu-bar controls
- **Cross-Platform** — Windows 10/11 and macOS 13+
- **Offline-First** — Core functionality works without internet

## Privacy Model

- **No cloud account required** for normal use
- **No webcam uploads** — All camera processing happens locally using OpenCV
  and MediaPipe
- **No raw video recording** by default — only derived metrics are stored
- **Local SQLite database** for all user data
- **User-controlled** — Export (JSON/CSV) or delete your data at any time
- **Transparent** — Camera status is always visible in the UI
- **Minimal telemetry** — None by default

## Supported Platforms

| Platform | Supported Versions |
|----------|-------------------|
| Windows  | 10, 11            |
| macOS    | 13+               |

## Prerequisites

### For Development

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.12+ (3.14 recommended) | Required for desktop app |
| Node.js | 20.9+ | Required for web app |
| npm | 9+ | Comes with Node.js |
| Git | any recent | For version control |

Optional:
- **Camera** — Required only for Smart Mode testing
- **PyInstaller** — Required for building desktop packages

### For End Users

No installation of Python, Node.js, or other development tools is required.
Download the appropriate installer for your platform from the releases page.

## Repository Structure

```
eye-health-assistant/
├── apps/
│   ├── desktop/              # Python + PySide6 desktop application
│   │   ├── src/              # Source code (eye_health_assistant package)
│   │   │   ├── app/          # Bootstrap, lifecycle, dependencies
│   │   │   ├── core/         # Config, constants, exceptions, logging
│   │   │   ├── domain/       # Models, enums, value objects, services
│   │   │   ├── application/  # Use cases, commands, queries, DTOs
│   │   │   ├── infrastructure/  # Database, camera, notifications
│   │   │   ├── monitoring/   # Monitoring engine
│   │   │   ├── blink/        # Blink detection
│   │   │   ├── timer/        # Timer engine
│   │   │   ├── analytics/    # Statistics, insights, scoring
│   │   │   ├── exercises/    # Exercise catalog
│   │   │   ├── content/      # Educational content loader
│   │   │   ├── settings/     # Settings management
│   │   │   ├── notifications/  # Notification service
│   │   │   └── ui/           # PySide6 UI (pages, widgets, themes)
│   │   ├── tests/            # Unit, integration, and e2e tests
│   │   ├── resources/        # Icons, images, stylesheets
│   │   └── pyproject.toml    # Python project config
│   └── web/                  # Next.js 16 landing website
│       ├── app/              # App router pages
│       ├── components/       # React components
│       ├── public/           # Static assets
│       └── package.json      # Node.js project config
├── packages/
│   ├── config/               # Shared configuration
│   ├── design-tokens/        # Visual design system tokens
│   └── docs/                 # Shared documentation
├── docs/                     # Project documentation
│   ├── architecture/
│   ├── development/
│   ├── privacy/
│   ├── release/
│   └── testing/
├── .github/workflows/        # CI/CD pipelines
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
├── LICENSE
└── Makefile
```

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/CoderSwarup/eye-health-assistant.git
cd eye-health-assistant
```

### 2. Install All Dependencies

```bash
make install
```

This installs both desktop (Python) and web (Node.js) dependencies.

Or install individually:

```bash
make install-desktop   # Python desktop app
make install-web      # Next.js web app
```

### 3. Python Installation (Manual)

If not using `make install`:

```bash
cd apps/desktop
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows
pip install -e ".[dev]"
```

For camera support (Smart Mode), also install:

```bash
pip install -e ".[camera]"
```

### 4. Node.js Installation (Manual)

If not using `make install`:

```bash
cd apps/web
npm install
```

## Running the Desktop App

```bash
make run-desktop
```

Or manually:

```bash
cd apps/desktop
source .venv/bin/activate
python -m eye_health_assistant
```

## Running the Web App

```bash
make run-web
```

Or manually:

```bash
cd apps/web
npm run dev
```

Then visit `http://localhost:3000`.

## Running Tests

### All Tests

```bash
make test
```

### Desktop Tests Only

```bash
make test-desktop
```

### Web Tests Only

```bash
make test-web
```

### Desktop Tests With Coverage

```bash
make test-coverage
```

### Verbose Output

```bash
cd apps/desktop && source .venv/bin/activate && pytest -v
```

### Specific Test File

```bash
cd apps/desktop && source .venv/bin/activate && pytest tests/unit/test_config.py -v
```

## Formatting and Linting

### Run All Quality Checks (lint + test)

```bash
make check
```

### Format All Code

```bash
make format
```

### Format Only Python

```bash
make format-python
```

### Format Only Web

```bash
make format-web
```

### Run All Linters

```bash
make lint
```

### Run Python Linters (ruff + mypy)

```bash
make lint-python
```

### Run Web Linters (eslint)

```bash
make lint-web
```

### Type Checking

```bash
make typecheck          # Both Python and web
make typecheck-python   # Python only (mypy)
make typecheck-web      # Web only (tsc --noEmit)
```

## Building Desktop Packages

### macOS

```bash
make build-desktop
```

This uses PyInstaller to create a standalone application bundle.

### Windows

The build must run on a Windows machine or CI runner:

```bash
make build-desktop
```

Build artifacts:
```
EyeHealthAssistant-Windows-x64-v1.0.0.exe
EyeHealthAssistant-macOS-arm64-v1.0.0.dmg
EyeHealthAssistant-macOS-x64-v1.0.0.dmg
```

## Building the Website

```bash
make build-web
```

Or:

```bash
cd apps/web && npm run build
```

The output is a static site in `apps/web/.next/` or `apps/web/out/`.

## Makefile Reference

Run `make help` to see all available commands:

```bash
make help
```

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make install` | Install all dependencies (desktop + web) |
| `make install-desktop` | Install Python desktop app dependencies |
| `make install-web` | Install Next.js web app dependencies |
| `make lint` | Run all linters (Python + web) |
| `make lint-python` | Run ruff and mypy |
| `make lint-web` | Run eslint |
| `make format` | Format all code |
| `make format-python` | Format Python with ruff |
| `make format-web` | Format web with prettier |
| `make typecheck` | Run all type checkers |
| `make typecheck-python` | Run mypy |
| `make typecheck-web` | Run tsc --noEmit |
| `make test` | Run all tests |
| `make test-desktop` | Run pytest |
| `make test-web` | Run vitest |
| `make test-coverage` | Run pytest with HTML coverage report |
| `make check` | Run lint + test (full quality check) |
| `make build` | Build all applications |
| `make build-desktop` | Build desktop with PyInstaller |
| `make build-web` | Build web with Next.js |
| `make clean` | Remove build artifacts and caches |

## Environment Variables

The desktop application works without environment variables for normal use.

### Desktop App

Copy the example file and adjust as needed:

```bash
cp apps/desktop/.env.example apps/desktop/.env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `EYE_HEALTH_LOG_LEVEL` | Logging level | `INFO` |
| `EYE_HEALTH_THEME` | UI theme (light/dark/system) | `system` |
| `EYE_HEALTH_CAMERA_INDEX` | Camera device index | `0` |

### Web App

Copy the example file and adjust as needed:

```bash
cp apps/web/.env.example apps/web/.env.local
```

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_SITE_URL` | Site URL for metadata | `http://localhost:3000` |
| `NEXT_PUBLIC_DOWNLOAD_WINDOWS_URL` | Windows download link | (empty) |
| `NEXT_PUBLIC_DOWNLOAD_MACOS_URL` | macOS download link | (empty) |

No API keys, secrets, or cloud credentials are required.

## Troubleshooting

### Camera Permission Denied

- **macOS**: System Preferences → Security & Privacy → Privacy → Camera →
  enable Eye Health Assistant
- **Windows**: Settings → Privacy → Camera → enable for Eye Health Assistant

### Camera Not Detected

- Ensure a camera is connected
- Check if another application is using the camera
- Try selecting a different camera in Settings → Camera

### App Not Starting

1. Check that Python 3.12+ is installed: `python3 --version`
2. Verify dependencies: `pip install -e ".[dev]"`
3. Check logs in the application data directory

### Database Issues

The SQLite database is stored in your platform's application data directory:
- **macOS**: `~/Library/Application Support/EyeHealthAssistant/database/`
- **Windows**: `AppData/Local/EyeHealthAssistant/database/`

Reset from Settings → Privacy → Delete All Data, or delete the database file.

### Notifications Not Appearing

- **macOS**: System Preferences → Notifications → Eye Health Assistant
- **Windows**: Settings → System → Notifications → Eye Health Assistant

### High CPU Usage

- Check if Smart Mode is running unnecessarily
- Reduce monitoring frequency in Settings → Monitoring

### "No module named eye_health_assistant.__main__"

The editable install was done before `__main__.py` was added. Reinstall:

```bash
make install-desktop
```

### Build Failures

- Ensure all dependencies are installed
- Run `make clean` and try again
- Check Python and Node.js versions meet minimum requirements

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to
contribute to this project.

Key points:
- Follow the layered architecture (UI → Application → Domain → Infrastructure)
- Write tests for business logic
- Never persist webcam frames
- Never make medical claims
- Use type hints in Python
- Run `make check` before submitting

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE)
file for details.

## Disclaimer

Eye Health Assistant is a wellness and educational tool. It is not intended to
diagnose, treat, cure, or prevent disease. If you experience persistent,
severe, painful, or concerning eye symptoms, the application encourages you to
seek advice from a qualified eye-care professional rather than relying on
application scores or reminders.
