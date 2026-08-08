# Contributing to Eye Health Assistant

Thank you for your interest in contributing to Eye Health Assistant! This document provides guidelines and information for contributors.

## Code of Conduct

Please be respectful and constructive in all interactions. We are building a privacy-first wellness tool and should treat our users and each other with care.

## Getting Started

### Prerequisites

- Python 3.12 or later (3.14 recommended)
- Node.js 18 or later
- npm or yarn
- Git

### Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/CoderSwarup/eye-health-assistant.git
   cd eye-health-assistant
   ```

2. Set up the Python desktop app:
   ```bash
   cd apps/desktop
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. Set up the web app:
   ```bash
   cd apps/web
   npm install
   ```

## Project Structure

This is a monorepo with two main applications:

- `apps/desktop` - Python desktop application (PySide6)
- `apps/web` - Next.js landing website
- `packages/` - Shared configuration and design tokens
- `docs/` - Project documentation

## Development Workflow

### Python Desktop App

- **Linting**: `ruff check .`
- **Formatting**: `ruff format .`
- **Type checking**: `mypy src/`
- **Tests**: `pytest`
- **Coverage**: `pytest --cov=eye_health_assistant`

### Web App

- **Linting**: `npm run lint`
- **Type checking**: `npm run typecheck`
- **Tests**: `npm test`
- **Build**: `npm run build`

### Running Quality Checks

From the project root:
```bash
make lint        # Run all linters
make test        # Run all tests
make format      # Format all code
make check       # Run all quality checks
```

## Architecture Guidelines

### Layered Architecture

The desktop application uses a layered architecture:

```
UI → Application → Domain → Infrastructure
```

- **UI**: Windows, pages, widgets, dialogs, themes
- **Application**: Use cases, commands, queries
- **Domain**: Business models, services, value objects
- **Infrastructure**: Database, camera, notifications, filesystem

### Key Rules

1. **No database queries in UI code**
2. **No computer vision algorithms in UI code**
3. **No business logic in UI widgets**
4. **Use type hints everywhere**
5. **Keep functions focused and small**
6. **Prevent composition over inheritance**
7. **Write tests for business logic**

### Privacy Rules

1. **Never persist webcam frames by default**
2. **Never upload camera data**
3. **Never make medical or diagnostic claims**
4. **Always use words like "estimated" for blink rate**
5. **User data stays local**
6. **Camera permission must be explicit**

## Commit Messages

Use clear, descriptive commit messages:

- `feat: add timer mode configuration`
- `fix: resolve camera permission dialog issue`
- `docs: update development setup guide`
- `test: add blink calculation unit tests`
- `refactor: extract notification service`

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes following the guidelines above
3. Run all quality checks (`make check`)
4. Update documentation if behavior changes
5. Submit a pull request with a clear description

## Testing Requirements

- **Unit tests** for all business logic
- **Integration tests** for repository and service interactions
- **No dependency on physical cameras** in tests
- Use mocks for camera and platform-specific code
- Aim for meaningful coverage, not just high percentages

## Documentation

- Update `docs/CHANGELOG.md` for user-facing changes
- Update relevant docs in `docs/` directory
- Add docstrings to public APIs
- Keep README.md current

## Questions?

If you have questions about contributing, please open an issue or reach out to the maintainers.
