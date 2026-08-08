# Development Setup Guide

## Prerequisites

### Required

- **Python 3.12+** (3.14 recommended)
- **Node.js 18+**
- **Git**

### Optional

- **Docker** (for containerized development)
- **VS Code** with Python and TypeScript extensions

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/CoderSwarup/eye-health-assistant.git
cd eye-health-assistant
```

### 2. Desktop Application Setup

```bash
cd apps/desktop

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run the application
python -m eye_health_assistant
```

### 3. Web Application Setup

```bash
cd apps/web

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. All Dependencies at Once

```bash
make install
```

## Development Commands

### Quality Checks

```bash
# Run all quality checks
make check

# Run only linting
make lint

# Run only tests
make test

# Format all code
make format
```

### Desktop-Specific

```bash
cd apps/desktop

# Run linting
ruff check .

# Run type checking
mypy src/

# Run tests
pytest

# Run tests with coverage
pytest --cov=eye_health_assistant --cov-report=html
```

### Web-Specific

```bash
cd apps/web

# Run linting
npm run lint

# Run type checking
npm run typecheck

# Run tests
npm test

# Build for production
npm run build
```

## IDE Setup

### VS Code

Recommended extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Ruff (charliermarsh.ruff)
- Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)
- ESLint (dbaeumer.vscode-eslint)

The workspace should automatically detect the Python virtual environment and TypeScript configuration.

## Architecture

See [Architecture Overview](../architecture/overview.md) for details on the layered architecture and design principles.

## Troubleshooting

### Camera Permission Issues

- **macOS**: System Preferences → Security & Privacy → Privacy → Camera
- **Windows**: Settings → Privacy → Camera

### Database Issues

The SQLite database is stored in your platform's application data directory. You can reset it from Settings → Privacy → Delete All Data, or by deleting the database file directly.

### Dependency Conflicts

If you encounter dependency conflicts:
1. Remove `__pycache__` directories: `find . -type d -name __pycache__ -exec rm -rf {} +`
2. Remove virtual environment and recreate it
3. Reinstall dependencies
