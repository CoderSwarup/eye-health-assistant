# CI/CD Pipeline

## Overview

GitHub Actions runs automated quality checks on every push and pull request.

## Pipelines

### Python Desktop Pipeline

```yaml
name: Desktop CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -e ".[dev]" --workdir apps/desktop
      - name: Lint
        run: cd apps/desktop && ruff check .
      - name: Type check
        run: cd apps/desktop && mypy src/
      - name: Test
        run: cd apps/desktop && pytest
```

### Web Pipeline

```yaml
name: Web CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install
        run: cd apps/web && npm ci
      - name: Lint
        run: cd apps/web && npm run lint
      - name: Type check
        run: cd apps/web && npm run typecheck
      - name: Test
        run: cd apps/web && npm test
      - name: Build
        run: cd apps/web && npm run build
```

### Security Pipeline

```yaml
name: Security
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Python audit
        run: pip install safety && safety check --workdir apps/desktop
      - name: npm audit
        run: cd apps/web && npm audit --audit-level=high
```

## Release Pipeline

See [Release Documentation](./release.md) for build artifact generation and release workflow.

## Branch Protection

- `main` branch requires all CI checks to pass
- Pull requests require at least one review
- Force push is restricted on `main`
