# Development Guide

## Quick Start

### Desktop App

```bash
cd apps/desktop
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -e ".[dev]"
python -m eye_health_assistant
```

### Web Landing Site

```bash
cd apps/web
npm install
npm run dev
```

## Project Structure

```
eye-health-assistant/
├── apps/
│   ├── desktop/          # Python + PySide6
│   │   ├── src/          # Source code
│   │   ├── tests/        # Unit + integration tests
│   │   ├── pyproject.toml
│   │   └── Makefile
│   └── web/              # Next.js 16
│       ├── app/          # App Router
│       ├── components/   # React components
│       ├── package.json
│       └── eslint.config.mjs
├── docs/                 # Documentation
├── .github/workflows/    # CI/CD
└── Makefile              # Root commands
```

## Common Commands

### Desktop Development

```bash
# Install dependencies
cd apps/desktop && pip install -e ".[dev]"

# Run linter
ruff check src/

# Run formatter
ruff format src/

# Run type checker
mypy src/

# Run tests
pytest tests/ -v

# Run all checks
make check
```

### Web Development

```bash
# Install dependencies
cd apps/web && npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Run linter
eslint .

# Run tests
npm test
```

## Testing

### Desktop Tests

```bash
# Run all tests
pytest tests/ -v

# Run unit tests only
pytest tests/unit/ -v

# Run with coverage
pytest tests/ --cov=eye_health_assistant

# Run specific test file
pytest tests/unit/test_config.py -v
```

### Web Tests

```bash
# Run all tests
npm test

# Run in watch mode
npm test -- --watch
```

## Code Quality

### Python (Desktop)
- **Linter**: Ruff (configured in `pyproject.toml`)
- **Type Checker**: mypy (configured in `pyproject.toml`)
- **Formatter**: Ruff format

### TypeScript/React (Web)
- **Linter**: ESLint 9 (flat config in `eslint.config.mjs`)
- **Type Checker**: TypeScript strict mode
- **Formatter**: Prettier (if configured)

## Architecture

### Desktop Layered Architecture

```
UI → Application → Domain → Infrastructure
```

- **UI**: PySide6 windows, pages, widgets, themes
- **Application**: Use cases, commands, queries, DTOs
- **Domain**: Models, enums, value objects, services
- **Infrastructure**: SQLite repos, camera adapters, notifications

### Web Architecture

- **App Router**: File-based routing with React Server Components
- **Components**: Reusable UI components (14 sections)
- **Styling**: Tailwind CSS v4 with design tokens

## Privacy Rules

1. **Never persist webcam frames** — process in memory only
2. **Never upload camera data** — all processing is local
3. **Never make medical claims** — use "estimated", "wellness"
4. **Camera permission must be explicit** — never silently request
5. **User data stays local** — no cloud accounts, no telemetry

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "feat: description"

# Push to remote
git push origin feature/your-feature

# Create PR on GitHub
gh pr create
```

## Troubleshooting

### Common Issues

**Desktop app won't start**
- Check Python version: `python --version`
- Reinstall dependencies: `pip install -e ".[dev]"`

**Web app build fails**
- Clear cache: `rm -rf .next`
- Reinstall: `rm -rf node_modules && npm install`

**Tests failing**
- Check environment variables
- Verify all dependencies installed
- Check test database permissions
