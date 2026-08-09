# Contributing to Eye Health Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

### Prerequisites

1. Git 2.30+
2. Python 3.12+ (for desktop app)
3. Node.js 20+ (for web app)
4. VS Code (recommended) with relevant extensions

### Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone git@github.com:your-username/eye-health-assistant.git
   ```
3. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```

## Development Workflow

### Desktop App (Python + PySide6)

```bash
cd apps/desktop
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Web App (Next.js)

```bash
cd apps/web
npm install
```

## Code Standards

### Python (Desktop)

- **Linter**: Ruff (configured in `pyproject.toml`)
- **Type Checker**: mypy
- **Formatter**: Ruff format
- **Style**: Follow PEP 8, use type hints

```bash
# Check code
ruff check src/
mypy src/

# Format code
ruff format src/
```

### TypeScript/React (Web)

- **Linter**: ESLint 9 (flat config)
- **Type Checker**: TypeScript strict mode
- **Formatter**: Prettier (if configured)

```bash
# Check code
eslint .

# Type check
tsc --noEmit
```

## Architecture Guidelines

### Desktop Layered Architecture

```
UI → Application → Domain → Infrastructure
```

- **UI**: No business logic, no database queries
- **Application**: Use cases, commands, queries
- **Domain**: Models, enums, services (no UI or infrastructure)
- **Infrastructure**: Database, camera, notifications

### Web Architecture

- **App Router**: File-based routing
- **Components**: Reusable, composable
- **Server Components**: Default for data fetching
- **Client Components**: Only when interactivity needed

## Privacy Rules (Non-Negotiable)

1. **Never persist webcam frames** — process in memory only
2. **Never upload camera data** — all processing is local
3. **Never make medical claims** — use "estimated", "wellness"
4. **Camera permission must be explicit** — never silently request
5. **User data stays local** — no cloud accounts, no telemetry

## Testing

### Desktop Tests

```bash
cd apps/desktop
pytest tests/ -v
```

### Web Tests

```bash
cd apps/web
npm test
```

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following the guidelines above
3. **Write tests** for new functionality
4. **Update documentation** if needed
5. **Run all checks**:
   ```bash
   # Desktop
   cd apps/desktop && make check
   
   # Web
   cd apps/web && npm run lint && npm test
   ```
6. **Commit with clear message**:
   ```bash
   git commit -m "feat: add new feature"
   ```
7. **Push and create PR**:
   ```bash
   git push origin feature/your-feature
   gh pr create
   ```

### PR Title Convention

- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation
- `style:` — Formatting, no code change
- `refactor:` — Code restructuring
- `test:` — Adding tests
- `chore:` — Maintenance

## Code Review

All PRs require:
1. **Passing CI** (lint, type check, tests)
2. **Code review** from maintainer
3. **No conflicts** with main branch

## Getting Help

- Check existing issues and documentation
- Open a discussion for questions
- Review the PRD at `docs/EYE_CARE_PRD.md`

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
