# Testing Guide

## Test Structure

```
tests/
├── unit/           # Isolated business logic tests
├── integration/    # Repository and service integration tests
└── e2e/            # End-to-end flow tests
```

## Running Tests

### All Tests

```bash
cd apps/desktop
pytest
```

### Unit Tests Only

```bash
pytest tests/unit/
```

### Integration Tests

```bash
pytest tests/integration/
```

### With Coverage

```bash
pytest --cov=eye_health_assistant --cov-report=html
open htmlcov/index.html
```

### Specific Test File

```bash
pytest tests/unit/test_blink_calculator.py
```

### Verbose Output

```bash
pytest -v
```

## Test Guidelines

### Unit Tests

- Test business logic in isolation
- Use mocks for external dependencies (camera, database, OS)
- Test both success and error paths
- Use descriptive test names

### Integration Tests

- Test repository implementations with real SQLite
- Test service interactions
- Use test fixtures for database setup/teardown

### Computer Vision Tests

- **Never depend on a physical camera**
- Use deterministic fixtures (pre-made images/video)
- Mock camera adapters
- Test scenarios: face detected, no face, eyes open, eyes closed, blink, etc.

### E2E Tests

- Test complete user flows
- Mock external systems
- Test first launch, onboarding, timer, monitoring, etc.

## Writing Tests

### Example Unit Test

```python
from eye_health_assistant.blink.calculator import BlinkCalculator

def test_blink_rate_calculation():
    calculator = BlinkCalculator(window_minutes=3)
    calculator.record_blinks(count=45, duration_seconds=180)
    rate = calculator.get_blink_rate()
    assert rate == 15.0  # 45 blinks / 3 minutes
```

### Example Integration Test

```python
import pytest
from eye_health_assistant.infrastructure.database.repositories import MonitoringRepository

@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "test.sqlite"
    return MonitoringRepository(db_path)

def test_create_session(repo):
    session = repo.create_session(mode="timer")
    assert session.id is not None
    assert session.mode == "timer"
```

## Coverage Targets

- Unit tests: 90%+ for business logic
- Integration tests: 80%+ for repositories
- Overall: 75%+ line coverage

## CI Integration

Tests run automatically in CI on every push and pull request. See [CI/CD documentation](../release/ci-cd.md) for details.
