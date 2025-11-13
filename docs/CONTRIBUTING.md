# Contributing to Nutrition Intelligence

Thank you for your interest in contributing to Nutrition Intelligence! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We pledge to:

- Be respectful and considerate
- Welcome diverse perspectives and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment, trolling, or discriminatory comments
- Personal attacks or insults
- Publishing others' private information
- Spam or off-topic content
- Any conduct that could be considered inappropriate in a professional setting

### Enforcement

Violations can be reported to the project maintainers at [conduct@ejemplo.com]. All complaints will be reviewed and investigated promptly and fairly.

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Git**: Version control
- **Node.js 16+**: For frontend development
- **Python 3.11+**: For backend development
- **Docker & Docker Compose**: For local development
- **Code editor**: VS Code recommended with extensions:
  - Python
  - ESLint
  - Prettier
  - Docker

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR-USERNAME/nutrition-intelligence.git
cd nutrition-intelligence
```

3. Add upstream remote:

```bash
git remote add upstream https://github.com/original-owner/nutrition-intelligence.git
```

4. Verify remotes:

```bash
git remote -v
# origin    https://github.com/YOUR-USERNAME/nutrition-intelligence.git (fetch)
# origin    https://github.com/YOUR-USERNAME/nutrition-intelligence.git (push)
# upstream  https://github.com/original-owner/nutrition-intelligence.git (fetch)
# upstream  https://github.com/original-owner/nutrition-intelligence.git (push)
```

### Setup Development Environment

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Setup pre-commit hooks
pre-commit install

# Configure environment
cp .env.example .env
# Edit .env with your configuration
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm start
```

#### Start Services

```bash
# From project root
docker-compose up -d db redis

# Or start everything with Docker
docker-compose up -d
```

### Verify Setup

```bash
# Backend health check
curl http://localhost:8000/health

# Frontend
# Open http://localhost:3005 in browser

# Run tests
cd backend && pytest
cd frontend && npm test
```

## Development Workflow

### Creating a Branch

Always create a feature branch from `main`:

```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### Branch Naming Conventions

Use descriptive branch names with prefixes:

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `perf/` - Performance improvements
- `chore/` - Maintenance tasks

**Examples:**
- `feature/add-barcode-scanner`
- `fix/recipe-search-crash`
- `docs/update-api-documentation`
- `refactor/optimize-database-queries`

### Making Changes

1. Make your changes in your feature branch
2. Follow [coding standards](#coding-standards)
3. Add/update tests as needed
4. Update documentation if applicable
5. Run tests locally
6. Commit with [conventional commits](#commit-guidelines)

### Keeping Your Branch Updated

Regularly sync with upstream:

```bash
# Fetch upstream changes
git fetch upstream

# Rebase your branch
git rebase upstream/main

# Or merge if you prefer
git merge upstream/main
```

## Coding Standards

### Python (Backend)

#### Style Guide

Follow **PEP 8** with these specifics:

```python
# Maximum line length: 100 characters
# Indentation: 4 spaces
# String quotes: Double quotes preferred

# Good
def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.

    Args:
        weight_kg: Body weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: 'male' or 'female'

    Returns:
        BMR in calories per day

    Raises:
        ValueError: If gender is not 'male' or 'female'
    """
    if gender == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    elif gender == "female":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    else:
        raise ValueError(f"Invalid gender: {gender}")

    return bmr
```

#### Type Hints

Use type hints for all functions:

```python
from typing import List, Dict, Optional, Union

def search_foods(
    query: str,
    grupo: Optional[str] = None,
    limit: int = 20
) -> List[Dict[str, Union[str, float]]]:
    """Search foods in SMAE database."""
    pass
```

#### Docstrings

Use Google-style docstrings:

```python
def create_meal_plan(user_id: int, calories: int, days: int) -> MealPlan:
    """
    Create a personalized meal plan.

    Args:
        user_id: User's database ID
        calories: Daily calorie target
        days: Plan duration in days

    Returns:
        MealPlan object with generated meals

    Raises:
        ValueError: If calories < 1200 or > 4000
        UserNotFoundError: If user_id doesn't exist

    Example:
        >>> plan = create_meal_plan(user_id=1, calories=2000, days=7)
        >>> print(plan.days[0].meals)
    """
    pass
```

#### Code Organization

```python
# 1. Standard library imports
import os
import sys
from datetime import datetime, timedelta

# 2. Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator

# 3. Local imports
from core.database import get_db
from core.auth import get_current_user
from domain.users.models import User
```

#### Tools

Run these before committing:

```bash
# Format code
black backend/

# Sort imports
isort backend/

# Type checking
mypy backend/

# Linting
flake8 backend/
pylint backend/

# Or use pre-commit hooks (recommended)
pre-commit run --all-files
```

### JavaScript/TypeScript (Frontend)

#### Style Guide

Follow **Airbnb JavaScript Style Guide** with these additions:

```javascript
// Use functional components with hooks
import React, { useState, useEffect } from 'react';

// Good
const FoodSearch = ({ onSelect }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query.length >= 3) {
      searchFoods(query);
    }
  }, [query]);

  const searchFoods = async (searchQuery) => {
    setLoading(true);
    try {
      const response = await api.get(`/foods/search?q=${searchQuery}`);
      setResults(response.data.results);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Buscar alimento..."
      />
      {loading ? <Spinner /> : <ResultsList results={results} />}
    </div>
  );
};

export default FoodSearch;
```

#### Component Structure

```javascript
// 1. Imports
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Button, TextField } from '@mui/material';

// 2. Component
const MyComponent = ({ prop1, prop2 }) => {
  // Hooks
  const [state, setState] = useState(null);

  // Event handlers
  const handleClick = () => {
    // ...
  };

  // Render
  return (
    <div>
      {/* JSX */}
    </div>
  );
};

// 3. PropTypes
MyComponent.propTypes = {
  prop1: PropTypes.string.isRequired,
  prop2: PropTypes.number,
};

// 4. Default props
MyComponent.defaultProps = {
  prop2: 0,
};

// 5. Export
export default MyComponent;
```

#### Naming Conventions

```javascript
// Components: PascalCase
const FoodDiary = () => { /* ... */ };

// Functions: camelCase
const calculateCalories = (foods) => { /* ... */ };

// Constants: UPPER_SNAKE_CASE
const API_BASE_URL = 'http://localhost:8000';

// Files:
// - Components: PascalCase (FoodDiary.js)
// - Utils: camelCase (dateUtils.js)
// - Constants: camelCase (apiConfig.js)
```

#### Tools

```bash
# Lint
npm run lint

# Fix linting issues
npm run lint:fix

# Format with Prettier
npm run format

# Type check (if using TypeScript)
npm run type-check
```

### SQL

```sql
-- Use uppercase for keywords
-- Use snake_case for table/column names
-- Always use explicit JOIN syntax

-- Good
SELECT
    u.id,
    u.full_name,
    COUNT(mp.id) AS meal_plan_count
FROM auth_users u
LEFT JOIN meal_plans mp ON u.id = mp.user_id
WHERE u.account_status = 'active'
    AND u.primary_role = 'patient'
GROUP BY u.id, u.full_name
ORDER BY meal_plan_count DESC
LIMIT 10;

-- Bad
select u.id, u.full_name, count(mp.id) from auth_users u, meal_plans mp
where u.id=mp.user_id and u.account_status='active';
```

### Docker

```dockerfile
# Use official base images
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Use non-root user
RUN useradd -m appuser
USER appuser

# Expose port
EXPOSE 8000

# Use exec form for CMD
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Testing Guidelines

### Backend Tests

#### Unit Tests

```python
import pytest
from services.nutrition import calculate_macros

def test_calculate_macros_weight_loss():
    """Test macro calculation for weight loss goal."""
    result = calculate_macros(
        calories=1800,
        goal="weight_loss"
    )

    assert result["protein_g"] == 135  # 30% of 1800 cal
    assert result["carbs_g"] == 180    # 40% of 1800 cal
    assert result["fats_g"] == 60      # 30% of 1800 cal
    assert result["protein_percentage"] == 30

def test_calculate_macros_invalid_calories():
    """Test that invalid calories raise ValueError."""
    with pytest.raises(ValueError):
        calculate_macros(calories=500, goal="weight_loss")
```

#### Integration Tests

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_foods_api():
    """Test food search endpoint."""
    response = client.get("/api/v1/foods/search?q=tortilla")

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
    assert "tortilla" in data["results"][0]["nombre"].lower()

def test_create_product_requires_auth():
    """Test that creating product requires authentication."""
    response = client.post("/api/v1/products", json={
        "codigo_barras": "123456",
        "nombre": "Test Product"
    })

    assert response.status_code == 401
```

#### Run Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_nutrition.py

# With coverage
pytest --cov=backend --cov-report=html

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

### Frontend Tests

#### Component Tests

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import FoodSearch from './FoodSearch';

test('renders search input', () => {
  render(<FoodSearch />);
  const input = screen.getByPlaceholderText(/buscar/i);
  expect(input).toBeInTheDocument();
});

test('calls API on search', async () => {
  const mockFetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ results: [] }),
    })
  );
  global.fetch = mockFetch;

  render(<FoodSearch />);
  const input = screen.getByPlaceholderText(/buscar/i);

  fireEvent.change(input, { target: { value: 'tortilla' } });

  await waitFor(() => {
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/foods/search?q=tortilla')
    );
  });
});
```

#### E2E Tests

```javascript
// tests/e2e/food-search.spec.js
import { test, expect } from '@playwright/test';

test('user can search and select food', async ({ page }) => {
  await page.goto('http://localhost:3005');

  // Login
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Navigate to food search
  await page.click('text=Recordatorio 24h');

  // Search for food
  await page.fill('input[placeholder*="Buscar"]', 'tortilla');
  await page.waitForSelector('.search-results');

  // Verify results
  const results = await page.$$('.search-result');
  expect(results.length).toBeGreaterThan(0);

  // Select first result
  await results[0].click();

  // Verify food added
  await expect(page.locator('.food-diary')).toContainText('tortilla');
});
```

#### Run Tests

```bash
# Unit tests
npm test

# E2E tests
npx playwright test

# With UI
npx playwright test --ui

# Specific test
npx playwright test food-search.spec.js
```

### Test Coverage

Maintain **>80% code coverage** for:
- New features
- Bug fixes
- Critical paths

Check coverage:

```bash
# Backend
pytest --cov=backend --cov-report=term-missing

# Frontend
npm run test:coverage
```

## Commit Guidelines

### Conventional Commits

Use the **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

#### Examples

```bash
# Feature
git commit -m "feat(foods): add barcode scanner support"

# Bug fix
git commit -m "fix(rag): handle empty responses gracefully"

# Documentation
git commit -m "docs(api): update authentication examples"

# With body
git commit -m "feat(meal-plans): add vegetarian meal options

- Add vegetarian flag to meal plan generation
- Filter recipes by dietary preferences
- Update database schema

Closes #123"
```

### Commit Best Practices

- **Atomic commits**: One logical change per commit
- **Clear messages**: Describe what and why, not how
- **Present tense**: "Add feature" not "Added feature"
- **Imperative mood**: "Fix bug" not "Fixes bug"
- **Reference issues**: Include issue number if applicable

```bash
# Good
git commit -m "fix(products): prevent duplicate barcode entries

Add uniqueness validation before saving products to prevent
database constraint errors.

Closes #456"

# Bad
git commit -m "fixed stuff"
```

## Pull Request Process

### Before Submitting

1. **Test your changes**:
   ```bash
   # Backend
   pytest

   # Frontend
   npm test
   npx playwright test
   ```

2. **Update documentation**:
   - API changes → Update `docs/API.md`
   - User features → Update `docs/USER_GUIDE.md`
   - Architecture changes → Update `docs/ARCHITECTURE.md`

3. **Update CHANGELOG** (if applicable):
   ```markdown
   ## [Unreleased]

   ### Added
   - Barcode scanner support for products

   ### Fixed
   - RAG chat handling of empty responses
   ```

4. **Rebase on main**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Squash commits** (if needed):
   ```bash
   git rebase -i HEAD~3  # Squash last 3 commits
   ```

### Creating Pull Request

1. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Go to GitHub and create Pull Request

3. Fill out the PR template:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Added barcode scanner component
- Integrated with backend API
- Updated user documentation

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing completed

## Screenshots (if applicable)
[Add screenshots here]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added and passing
- [ ] No new warnings

## Related Issues
Closes #123
```

4. Request reviews from maintainers

### Review Process

- **Automated checks**: CI/CD pipeline runs
- **Code review**: At least 1 approval required
- **Discussion**: Address feedback promptly
- **Updates**: Push changes to same branch

### After Approval

1. **Squash and merge** (preferred) or **Rebase and merge**
2. **Delete branch** after merge
3. **Update local main**:
   ```bash
   git checkout main
   git pull upstream main
   ```

## Documentation

### When to Update Docs

- **New features**: Add to USER_GUIDE.md
- **API changes**: Update API.md
- **Architecture changes**: Update ARCHITECTURE.md
- **Deployment changes**: Update DEPLOYMENT.md
- **Bug fixes**: Update if user-facing

### Documentation Style

- **Clear and concise**: Simple language
- **Examples**: Provide code examples
- **Screenshots**: Add for UI features
- **Up-to-date**: Keep in sync with code
- **Accessible**: Consider all user levels

## Community

### Getting Help

- **GitHub Discussions**: Ask questions, share ideas
- **GitHub Issues**: Report bugs, request features
- **Email**: soporte@ejemplo.com
- **Discord** (if available): Real-time chat

### Reporting Bugs

Use the bug report template:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 10]
 - Browser: [e.g. chrome, safari]
 - Version: [e.g. 22]

**Additional context**
Any other information about the problem.
```

### Feature Requests

Use the feature request template:

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Other solutions you've thought about.

**Additional context**
Any other information or screenshots.
```

### Communication Guidelines

- **Be respectful**: Assume good intentions
- **Be patient**: Maintainers are volunteers
- **Be specific**: Provide details and context
- **Be responsive**: Reply to questions promptly
- **Be collaborative**: We're all learning

---

Thank you for contributing to Nutrition Intelligence! Your efforts help improve nutrition for everyone. 🌮❤️

**Questions?** Open a GitHub Discussion or email soporte@ejemplo.com

**Last Updated**: 2025-11-11
**Contributing Guide Version**: 1.0.0
