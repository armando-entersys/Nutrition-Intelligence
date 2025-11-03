# Testing Suite - Nutrition Intelligence Platform

## Overview

This directory contains comprehensive tests for the Nutrition Intelligence Platform, following the test matrix defined in `TESTING_PLAN.md`.

## Test Structure

```
tests/
├── conftest.py                          # Shared fixtures and test configuration
├── unit/                                # Unit tests (isolated component testing)
│   ├── __init__.py
│   └── test_laboratory_models.py       # 5+ unit tests for laboratory models
├── integration/                         # Integration tests (API endpoint testing)
│   ├── __init__.py
│   ├── test_laboratory_api.py          # 5+ integration tests for lab API
│   └── test_whatsapp_api.py            # 5+ integration tests for WhatsApp API
└── reports/                             # Generated test reports (HTML, coverage)
```

## Test Coverage

### Unit Tests (UT-LAB-001 to UT-LAB-005)
- **test_laboratory_models.py**: 10 unit tests covering:
  - UT-LAB-001: Valid laboratory data creation
  - UT-LAB-002: Out-of-range value validation and alerts
  - UT-LAB-003: Automatic HOMA-IR calculation
  - UT-LAB-004: Diabetes detection via HbA1c ≥ 6.5%
  - UT-LAB-005: High atherogenic index detection
  - Plus additional edge cases and derived calculations

### Integration Tests

#### Laboratory API (IT-LAB-001 to IT-LAB-005)
- **test_laboratory_api.py**: 12+ integration tests covering:
  - IT-LAB-001: Create complete laboratory record (POST /api/v1/laboratory/)
  - IT-LAB-002: Get patient labs with pagination (GET /api/v1/laboratory/patient/{id})
  - IT-LAB-003: Update laboratory values (PUT /api/v1/laboratory/{id})
  - IT-LAB-004: Laboratory trends analysis (GET /api/v1/laboratory/trends/patient/{id})
  - IT-LAB-005: Delete laboratory record (DELETE /api/v1/laboratory/{id})
  - Plus error handling and edge cases

#### WhatsApp API (IT-WA-001 to IT-WA-005)
- **test_whatsapp_api.py**: 15+ integration tests covering:
  - IT-WA-001: Send appointment reminder
  - IT-WA-002: Send meal plan notification with Twilio SID
  - IT-WA-003: Get message history with pagination
  - IT-WA-004: Create message template
  - IT-WA-005: Validation of invalid phone numbers
  - Plus template management and all message types

## Running Tests

### Prerequisites

```bash
# Install test dependencies (from backend/)
pip install pytest pytest-asyncio pytest-cov pytest-html httpx

# Or install all requirements
pip install -r requirements.txt
```

### Run All Tests

```bash
# From backend/ directory
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov=. --cov-report=html
```

### Run Specific Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only laboratory tests
pytest -m laboratory

# Run only WhatsApp tests
pytest -m whatsapp

# Run specific test file
pytest tests/unit/test_laboratory_models.py

# Run specific test class
pytest tests/unit/test_laboratory_models.py::TestLaboratoryDataModels

# Run specific test
pytest tests/unit/test_laboratory_models.py::TestLaboratoryDataModels::test_create_valid_laboratory_data
```

### Run with Different Output Formats

```bash
# Generate HTML report
pytest --html=tests/reports/test-report.html --self-contained-html

# Generate coverage report
pytest --cov=. --cov-report=html:tests/reports/coverage

# Show detailed output
pytest -vv

# Show only failed tests
pytest --tb=short --maxfail=1

# Run in parallel (requires pytest-xdist)
pytest -n auto
```

## Test Markers

Tests are marked with pytest markers for easy filtering:

- `@pytest.mark.unit` - Unit tests (isolated component tests)
- `@pytest.mark.integration` - Integration tests (API endpoint tests)
- `@pytest.mark.laboratory` - Laboratory module tests
- `@pytest.mark.whatsapp` - WhatsApp messaging tests
- `@pytest.mark.asyncio` - Async tests (automatically detected)

## Fixtures

Common fixtures defined in `conftest.py`:

- `test_session` - Async database session for testing
- `client` - AsyncClient for API testing
- `sample_patient` - Pre-created patient for testing
- `sample_lab_data_dict` - Normal laboratory data dictionary
- `sample_lab_data_high_values` - Laboratory data with high values for alert testing
- `sample_whatsapp_message_dict` - WhatsApp message data

## Test Database

Tests use a SQLite in-memory database (`sqlite+aiosqlite:///./test.db`) that is:
- Created fresh for each test session
- Automatically populated with required tables
- Cleaned up after tests complete

## Code Coverage Goals

| Component | Minimum Coverage | Target Coverage |
|-----------|-----------------|-----------------|
| Models & Schemas | 80% | 95% |
| API Endpoints | 85% | 95% |
| Services | 90% | 98% |
| **Overall Backend** | **85%** | **95%** |

## Test Reports

After running tests, reports are generated in `tests/reports/`:

- `test-report.html` - HTML test results with pass/fail details
- `coverage/index.html` - Code coverage report
- View in browser: `open tests/reports/test-report.html`

## Continuous Integration

Tests are configured to run in CI/CD pipeline:

```yaml
# Example CI configuration
stages:
  - unit-tests
  - integration-tests

unit-tests:
  script:
    - pytest -m unit --cov --cov-report=xml

integration-tests:
  script:
    - pytest -m integration
  dependencies:
    - unit-tests
```

## Writing New Tests

### Unit Test Template

```python
import pytest
from domain.module.models import YourModel

@pytest.mark.unit
class TestYourModel:
    """Unit tests for YourModel"""

    def test_your_feature(self):
        """Test description following UT-XXX-NNN format"""
        # Arrange
        data = {...}

        # Act
        result = YourModel(**data)

        # Assert
        assert result.field == expected_value
```

### Integration Test Template

```python
import pytest
from httpx import AsyncClient

@pytest.mark.integration
@pytest.mark.asyncio
class TestYourAPI:
    """Integration tests for Your API"""

    async def test_your_endpoint(self, client: AsyncClient):
        """Test description following IT-XXX-NNN format"""
        # Arrange
        payload = {...}

        # Act
        response = await client.post("/api/endpoint", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["field"] == expected_value
```

## Troubleshooting

### Import Errors

If you see import errors, ensure you're running from the `backend/` directory:

```bash
cd backend/
pytest
```

### Database Errors

If database tests fail, check:
1. SQLite is installed
2. Test database directory has write permissions
3. No other processes are using the test database

### Async Errors

If async tests fail:
1. Ensure `pytest-asyncio` is installed
2. Check `asyncio_mode = auto` is in `pytest.ini`
3. Use `@pytest.mark.asyncio` decorator on async tests

### Missing Fixtures

If fixtures are not found:
1. Ensure `conftest.py` is in the correct location
2. Check fixture name spelling
3. Verify fixture scope is correct

## Best Practices

1. **Isolation**: Each test should be independent
2. **AAA Pattern**: Arrange, Act, Assert structure
3. **Descriptive Names**: Test names should describe what they test
4. **Documentation**: Include docstrings with test ID references
5. **Cleanup**: Tests should clean up after themselves
6. **Mocking**: Mock external services (Twilio, databases) when appropriate
7. **Coverage**: Aim for >85% code coverage

## Related Documentation

- `TESTING_PLAN.md` - Comprehensive testing strategy and test matrix
- `pytest.ini` - Pytest configuration
- `conftest.py` - Shared test fixtures and setup

## Support

For questions about tests:
1. Check test docstrings for specific test case details
2. Review `TESTING_PLAN.md` for test requirements
3. Check CI/CD pipeline logs for test failures
4. Contact the development team

---

**Last Updated**: November 2, 2025
**Test Framework**: pytest 7.4.3
**Python Version**: 3.11+
