# CI/CD Workflows

This directory contains GitHub Actions workflow files that automate quality checks for the Eye Health Assistant project.

## Workflows

### `desktop-ci.yml` — Desktop App Quality Checks

**Trigger:** Push to `main` or pull request targeting `main`.

**What it does:**

| Step | Purpose |
|------|---------|
| 📥 Checkout | Clone the repository |
| 🐍 Set up Python | Install Python 3.13/3.14 on the runner |
| 💾 Cache pip | Cache downloaded packages to speed up future runs |
| 📦 Install dependencies | `pip install -e ".[dev]"` — install the desktop app in editable mode with dev extras |
| 🔍 Lint with Ruff | Check Python code for style errors, unused imports, formatting issues |
| 🏷️ Type check with mypy | Verify all type hints are correct, catch type-related bugs |
| 🧪 Run tests with coverage | Execute pytest and generate a coverage report (what % of code is tested) |
| ☁️ Upload coverage | Send coverage report to Codecov dashboard (optional, requires token) |

**Matrix:** Runs on Ubuntu, macOS, and Windows with Python 3.13 and 3.14 to ensure cross-platform compatibility.

---

### `web-ci.yml` — Web App Quality Checks

**Trigger:** Push to `main` or pull request targeting `main`.

**What it does:**

| Step | Purpose |
|------|---------|
| 📥 Checkout | Clone the repository |
| 🟢 Set up Node.js | Install Node.js 24 LTS on the runner |
| 📦 Install dependencies | `npm ci` — clean install from lockfile (deterministic) |
| 🔍 Lint with ESLint | Check TypeScript/React code for errors and style issues |
| 🏷️ Type check with TypeScript | Verify all types are correct with strict mode |
| 🧪 Run tests with Vitest | Execute unit tests |
| 🏗️ Build for production | Build the Next.js app to catch build errors early |

---

### `security.yml` — Dependency Security Audit

**Trigger:** Pull request targeting `main` + monthly schedule (1st of each month).

**What it does:**

| Step | Purpose |
|------|---------|
| 📥 Checkout | Clone the repository |
| 🐍 Set up Python | Install Python for pip-audit |
| 📦 Install pip-audit | Tool that scans Python packages for known vulnerabilities |
| 🔒 Audit Python dependencies | Check if any installed package has a known security issue |
| 🟢 Set up Node.js | Install Node.js for npm audit |
| 🔒 Audit npm dependencies | Check if any npm package has a known security issue |

**Why monthly?** Even without code changes, new vulnerabilities are discovered in existing packages. Monthly audits catch these.

**Why pull request only?** Security audits don't need to run on every push to main — they only need to verify that proposed changes don't introduce vulnerable dependencies.

---

## Why These Three Files?

| File | Catches | Runs When |
|------|---------|-----------|
| `desktop-ci.yml` | Python bugs, type errors, failing tests | Every push and PR |
| `web-ci.yml` | TypeScript errors, React issues, build failures | Every push and PR |
| `security.yml` | Vulnerable dependencies | PRs + monthly |

Together they ensure:
- **No broken code** reaches `main`
- **No type errors** ship to users
- **No known security vulnerabilities** in dependencies
- **Cross-platform compatibility** (Windows, macOS, Linux)

---

## Environment Requirements

| Tool | Version | Used By |
|------|---------|---------|
| Python | 3.13, 3.14 | Desktop CI, Security |
| Node.js | 24 LTS | Web CI, Security |
| Ruff | Latest | Desktop CI |
| mypy | Latest | Desktop CI |
| pytest | Latest | Desktop CI |
| ESLint | 9.x | Web CI |
| TypeScript | 5.7+ | Web CI |
| Vitest | 3.x | Web CI |

---

## Codecov (Optional)

The desktop CI uploads a coverage report to [Codecov](https://codecov.io). To enable:

1. Create a free account at codecov.io
2. Add your repository
3. Go to GitHub repo → Settings → Secrets and variables → Actions
4. Add a new secret: `CODECOV_TOKEN` with your token value

Without the token, the upload step silently succeeds without sending data. The coverage report still appears in the CI logs via `--cov-report=term-missing`.

---

## Local Reproduction

To run the same checks locally before pushing:

```bash
# Desktop checks
cd apps/desktop
ruff check .
mypy src/
pytest --cov=eye_health_assistant --cov-report=term-missing -v

# Web checks
cd apps/web
npm run lint
npm run typecheck
npm test
npm run build

# Or from project root
make check   # Runs all linters + tests
```

---

## Adding a New Workflow

1. Create a `.yml` file in `.github/workflows/`
2. Follow the naming convention: `{purpose}-ci.yml`
3. Use the same step structure (checkout → setup → cache → install → check)
4. Add emoji prefixes to step names for consistency
5. Add echo logs before and after each command
6. Test by pushing to a branch and opening a PR
