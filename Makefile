PYTHON = cd apps/desktop && .venv/bin/python3
PIP = cd apps/desktop && .venv/bin/pip3

.PHONY: help setup install install-desktop install-web run run-desktop run-web lint lint-python lint-web format format-python format-web typecheck typecheck-python typecheck-web test test-desktop test-web test-coverage check build build-desktop build-web clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv and install all dependencies
	cd apps/desktop && python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
	cd apps/web && npm install

install: install-desktop install-web ## Install all dependencies

install-desktop: ## Install desktop app dependencies
	cd apps/desktop && .venv/bin/pip3 install -e ".[dev]"

install-web: ## Install web app dependencies
	cd apps/web && npm install

run: run-desktop ## Run all applications

run-desktop: ## Run desktop app
	$(PYTHON) -m eye_health_assistant

run-web: ## Run web app (dev server)
	cd apps/web && npm run dev

lint: lint-python lint-web ## Run all linters

lint-python: ## Run Python linters (ruff + mypy)
	cd apps/desktop && .venv/bin/ruff check .
	cd apps/desktop && .venv/bin/mypy src/

lint-web: ## Run web linters (eslint)
	cd apps/web && npx eslint .

format: format-python format-web ## Format all code

format-python: ## Format Python code (ruff)
	cd apps/desktop && .venv/bin/ruff format .
	cd apps/desktop && .venv/bin/ruff check --fix .

format-web: ## Format web code (prettier)
	cd apps/web && npm run format

typecheck: typecheck-python typecheck-web ## Run all type checkers

typecheck-python: ## Run Python type checker (mypy)
	cd apps/desktop && .venv/bin/mypy src/

typecheck-web: ## Run web type checker (tsc)
	cd apps/web && npm run typecheck

test: test-desktop test-web ## Run all tests

test-desktop: ## Run desktop app tests (pytest)
	cd apps/desktop && .venv/bin/pytest

test-web: ## Run web app tests (vitest)
	cd apps/web && npm test

test-coverage: ## Run desktop tests with HTML coverage report
	cd apps/desktop && .venv/bin/pytest --cov=eye_health_assistant --cov-report=html

check: lint test ## Run all quality checks (lint + test)

build: build-desktop ## Build all applications

build-desktop: ## Build desktop app (PyInstaller)
	cd apps/desktop && .venv/bin/pyinstaller --windowed --name EyeHealthAssistant src/eye_health_assistant/main.py

build-web: ## Build web app (Next.js)
	cd apps/web && npm run build

clean: ## Clean build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	cd apps/web && rm -rf .next out node_modules 2>/dev/null || true
