# TTRPG Dice Roller - Development Plan

This document outlines the complete development plan for structuring the TTRPG Dice Roller Claude Skill project with modern tooling, testing infrastructure, and automated CI/CD.

## Current State

```
ttrpg-dice-roller/
├── src/
│   ├── SKILL.md
│   └── scripts/
│       └── dice_roller.py
├── README.md
├── LICENSE.txt
└── .gitignore
```

## Target State

```
ttrpg-dice-roller/
├── .github/
│   └── workflows/
│       ├── test.yml              # CI testing on push/PR
│       └── release.yml           # Auto-build zip on release
├── src/
│   ├── SKILL.md
│   └── scripts/
│       └── dice_roller.py
├── tests/
│   ├── __init__.py
│   ├── test_parser.py            # Basic parsing tests
│   ├── test_evaluator.py         # Dice evaluation tests
│   ├── test_modifiers.py         # Keep/drop/reroll/explode tests
│   ├── test_success_counting.py  # Success threshold tests
│   ├── test_fate.py              # FATE dice tests
│   ├── test_complex.py           # Complex expressions
│   ├── test_errors.py            # Error handling tests
│   └── test_statistical.py       # Randomness validation
├── .gitignore
├── .pre-commit-config.yaml       # Optional: pre-commit hooks
├── LICENSE.txt
├── README.md
├── PLAN.md                       # This file
├── pyproject.toml                # Project configuration
└── uv.lock                       # UV lock file (generated)
```

## Phase 1: Project Configuration

### 1.1 Initialize UV

```bash
# Verify installation
uv --version
```

### 1.2 Initialize UV Project

```bash
# Initialize UV in the existing project
uv init --no-readme

# Install development dependencies
uv add --dev pytest pytest-cov ruff
```

### 1.3 Create pyproject.toml

Create the following file:

```toml
[project]
name = "ttrpg-dice-roller"
version = "1.0.0"
description = "TTRPG dice roller Claude skill with CSPRNG"
authors = [
    {name = "Optional Rule Games"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.8"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "--verbose",
    "--cov=src/scripts",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = []
```

### 1.4 Update .gitignore

The `.gitignore` is already well-configured. No changes needed - it already includes:
- Test coverage directories (`htmlcov/`, `.coverage`, `.pytest_cache/`)
- Build artifacts (`dist/`, `build/`, `*.egg-info/`)
- Ruff cache (`.ruff_cache/`)

Note: `uv.lock` should be committed to version control for reproducibility (already correctly excluded from gitignore).

## Phase 2: Test Infrastructure

### 2.1 Create Test Directory Structure

```bash
mkdir -p tests
touch tests/__init__.py
```

### 2.2 Create Test Files

Create the following test files in the `tests/` directory:

#### tests/test_parser.py

Tests for basic dice notation parsing:
- Simple dice expressions (3d6, d20, 2d8+5)
- Percentile dice (d%, d00)
- Invalid syntax handling
- Edge cases

#### tests/test_evaluator.py

Tests for dice evaluation:
- Correct value ranges
- Arithmetic operations
- Grouping with parentheses
- Multiple dice terms

#### tests/test_modifiers.py

Tests for dice modifiers:
- Keep highest/lowest (kh, kl)
- Drop highest/lowest (dh, dl)
- Reroll (r, ro, r<N, r>N)
- Explosions (!, !p, !!, !>=N)
- Sorting (sa, sd)

#### tests/test_success_counting.py

Tests for success counting:
- Greater than/equal (>=, >)
- Less than/equal (<=, <)
- Exact match (=)
- Success counting mode vs sum mode

#### tests/test_fate.py

Tests for FATE/Fudge dice:
- 4dF basic rolls
- FATE with modifiers (4dF+3)
- Value ranges (-4 to +4)

#### tests/test_complex.py

Tests for complex expressions:
- Nested parentheses
- Multiple dice types in one expression
- Combined modifiers
- Order of operations

#### tests/test_errors.py

Tests for error handling:
- ParseError with position info
- SemanticError for invalid rules
- LimitError for safety limits
- Clear error messages

#### tests/test_statistical.py

Tests for statistical properties:
- Distribution uniformity
- No bias in results
- Randomness (non-deterministic)
- CSPRNG verification

### 2.3 Example Test File Template

Each test file should follow this pattern:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'scripts'))

import pytest
from dice_roller import roll_dice


class TestCategory:
    """Description of test category"""
    
    def test_specific_case(self):
        """Test a specific case"""
        result = roll_dice("3d6")
        assert result["ok"] is True
        assert 3 <= result["final"] <= 18
```

## Phase 3: GitHub Actions CI/CD

### 3.1 Create Workflows Directory

```bash
mkdir -p .github/workflows
```

### 3.2 Create Test Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  pull-requests: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
      
      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: uv sync --all-extras
      
      - name: Run tests
        run: uv run pytest
      
      - name: Run linter
        run: uv run ruff check src/
      
      - name: Upload coverage
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v3
        with:
          fail_ci_if_error: false
```

### 3.3 Create Release Workflow

Create `.github/workflows/release.yml`:

```yaml
name: Build and Release Skill Package

on:
  release:
    types: [created]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Create skill package
        run: |
          cd src
          zip -r ../ttrpg-dice-roller.zip . -x "*.git*" -x "*__pycache__*" -x "*.pyc"
      
      - name: Upload Release Asset
        env:
          GH_TOKEN: ${{ github.token }}
        run: gh release upload ${{ github.event.release.tag_name }} ttrpg-dice-roller.zip --clobber
```

## Phase 4: Documentation Updates

### 4.1 Update README.md

Add a "Development" section to README.md:

```markdown
## Development

### Setup

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/OptionalRule/ttrpg-dice-claude-skill.git
cd ttrpg-dice-roller

# Install dependencies
uv sync --all-extras
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_parser.py

# Run tests for specific pattern
uv run pytest -k "test_keep"
```

### Code Quality

```bash
# Check code style
uv run ruff check src/

# Auto-fix style issues
uv run ruff check --fix src/

# Format code
uv run ruff format src/
```

### Building the Skill Package

For local testing only (official releases are built automatically by GitHub Actions):

```bash
# Build manually
cd src
zip -r ../ttrpg-dice-roller.zip . -x "*.git*" -x "*__pycache__*" -x "*.pyc"
cd ..
# Package is now at ttrpg-dice-roller.zip
```

For official releases, create a GitHub release and the zip is built automatically.
```

### 4.2 Update Download Instructions

Replace the download section in README.md with:

```markdown
### Download the Skill

**Latest Release:** Download `ttrpg-dice-roller.zip` from:

```
https://github.com/OptionalRule/ttrpg-dice-claude-skill/releases/latest/download/ttrpg-dice-roller.zip
```

Or visit the [Releases](https://github.com/OptionalRule/ttrpg-dice-claude-skill/releases) page.
```

## Phase 5: Optional Enhancements

### 5.1 Pre-commit Hooks (Optional)

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
```

Install pre-commit hooks:

```bash
uv add --dev pre-commit
uv run pre-commit install
```

### 5.2 Coverage Badge

Add to README.md if using codecov:

```markdown
[![codecov](https://codecov.io/gh/OptionalRule/ttrpg-dice-claude-skill/branch/main/graph/badge.svg)](https://codecov.io/gh/OptionalRule/ttrpg-dice-claude-skill)
```

### 5.3 GitHub Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md` for structured issue reporting.

## Execution Checklist

### Phase 1: Setup
- [ ] Install UV package manager
- [ ] Run `uv init --no-readme`
- [ ] Run `uv add --dev pytest pytest-cov ruff`
- [ ] Create `pyproject.toml` with configuration
- [ ] Verify `.gitignore` is properly configured (already done)
- [ ] Commit changes: "chore: add UV and project configuration"

### Phase 2: Testing
- [ ] Create `tests/` directory
- [ ] Create `tests/__init__.py`
- [ ] Write `tests/test_parser.py`
- [ ] Write `tests/test_evaluator.py`
- [ ] Write `tests/test_modifiers.py`
- [ ] Write `tests/test_success_counting.py`
- [ ] Write `tests/test_fate.py`
- [ ] Write `tests/test_complex.py`
- [ ] Write `tests/test_errors.py`
- [ ] Write `tests/test_statistical.py`
- [ ] Run `uv run pytest` to verify tests pass
- [ ] Run `uv run pytest --cov` to check coverage
- [ ] Commit changes: "test: add comprehensive test suite"

### Phase 3: CI/CD
- [ ] Create `.github/workflows/` directory
- [ ] Create `.github/workflows/test.yml`
- [ ] Create `.github/workflows/release.yml`
- [ ] Push to GitHub to trigger CI
- [ ] Verify tests run on push
- [ ] Commit changes: "ci: add GitHub Actions workflows"

### Phase 4: Documentation
- [ ] Add "Development" section to README.md
- [ ] Update download instructions with persistent URL
- [ ] Add testing commands to README.md
- [ ] Update project structure in README.md
- [ ] Commit changes: "docs: add development documentation"

### Phase 5: Release Testing
- [ ] Create a test release tag: `git tag v1.0.0-test`
- [ ] Push tag: `git push origin v1.0.0-test`
- [ ] Create GitHub release from tag
- [ ] Verify release workflow builds and attaches zip
- [ ] Test download URL works
- [ ] Delete test release if successful

### Phase 6: Optional Enhancements
- [ ] Add pre-commit hooks configuration
- [ ] Install pre-commit: `uv run pre-commit install`
- [ ] Add coverage badge to README.md
- [ ] Create GitHub issue templates
- [ ] Commit changes: "chore: add optional tooling"

## Testing Commands Reference

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src/scripts --cov-report=html

# Run specific test file
uv run pytest tests/test_parser.py

# Run specific test class
uv run pytest tests/test_parser.py::TestBasicParsing

# Run specific test method
uv run pytest tests/test_parser.py::TestBasicParsing::test_simple_dice

# Run tests matching pattern
uv run pytest -k "keep"

# Run tests and stop on first failure
uv run pytest -x

# Show print statements
uv run pytest -s

# Run linter
uv run ruff check src/

# Fix linting issues
uv run ruff check --fix src/

# Format code
uv run ruff format src/
```

## Continuous Integration Verification

After pushing to GitHub, verify:

1. **Test workflow runs** on push to main/develop
2. **Tests pass** across all Python versions (3.8-3.12)
3. **Linting passes** with no errors
4. **Release workflow** creates zip file when release is created
5. **Download URL** works: `https://github.com/OptionalRule/ttrpg-dice-claude-skill/releases/latest/download/ttrpg-dice-roller.zip`

## Benefits of This Structure

### For Users
- **Persistent download URL** - Always get latest version
- **Verified releases** - CI ensures package builds correctly
- **Transparent testing** - See test results in PRs

### For Developers
- **Automated testing** - Tests run on every push
- **Multi-version support** - Tests across Python 3.8-3.12
- **Code quality** - Linting enforced automatically
- **Easy setup** - `uv sync` installs everything needed
- **Fast testing** - UV caches dependencies

### For Contributors
- **Clear standards** - Ruff enforces code style
- **Immediate feedback** - CI runs tests on PRs
- **Test examples** - Comprehensive test suite to learn from
- **Documentation** - Clear dev setup instructions

## Migration Notes

### Build Process

This project does not include a `build.py` script. GitHub Actions automatically builds the skill package on every release. For local testing, developers can manually run the zip command (see "Building the Skill Package" section above).

### Backward Compatibility

All changes are additive:
- Existing `src/` structure unchanged
- No breaking changes to the skill itself
- Users don't need to know about dev tooling
- Manual zip command available for local testing

## Success Criteria

Project is considered successfully restructured when:

1. ✅ `uv run pytest` passes all tests
2. ✅ `uv run ruff check src/` shows no errors
3. ✅ GitHub Actions CI passes on push
4. ✅ GitHub Actions Release workflow creates zip file
5. ✅ Persistent download URL works
6. ✅ Test coverage is >70%
7. ✅ Documentation is complete and accurate
8. ✅ All Python versions (3.8-3.12) pass tests

## Next Steps After Completion

1. **Create first official release** (v1.0.0)
2. **Add badges** to README (build status, coverage)
3. **Write CONTRIBUTING.md** with guidelines for contributors
4. **Add example notebooks** for testing/demonstration
5. **Set up GitHub Pages** for documentation (optional)
6. **Add performance benchmarks** (optional)
7. **Create video tutorial** for skill usage (optional)

---

**Timeline Estimate:** 2-4 hours for full implementation

**Priority:** High - Improves maintainability and contributor experience

**Dependencies:** UV, GitHub account with Actions enabled

**Risk:** Low - All changes are additive and backward compatible