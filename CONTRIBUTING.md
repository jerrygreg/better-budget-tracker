# 🤝 Contributing to Budget Planner & Financial Goals Tracker

Thank you for your interest in contributing to the Budget Planner & Financial Goals Tracker! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Contribution Guidelines](#contribution-guidelines)
- [Priority TODOs](#priority-todos)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Release Process](#release-process)

## 📜 Code of Conduct

This project follows a code of conduct that ensures a welcoming environment for all contributors. Please:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- Basic knowledge of Python, SQLite, and CLI applications

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/budget-tracker.git
   cd budget-tracker
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/originalowner/budget-tracker.git
   ```

## 🛠️ Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 3. Verify Installation

```bash
# Run the application
python main.py

# Run the demo
python demo.py

# Run tests (if available)
pytest
```

## 📁 Project Structure

```
budget_tracker/
├── main.py                 # CLI entry point
├── budget.py               # Income, expense, and budget management
├── goal_tracker.py         # Savings goals tracking
├── reports.py              # Report generation and charts
├── utils.py                # Utility functions
├── demo.py                 # Demo script
├── data/                   # Database storage
│   └── budget_data.db      # SQLite database
├── reports/                # Generated reports
├── tests/                  # Test files (to be created)
├── requirements.txt        # Dependencies
├── README.md              # Project documentation
└── CONTRIBUTING.md        # This file
```

### Module Responsibilities

- **`main.py`**: CLI interface, user interaction, menu handling
- **`budget.py`**: Income/expense CRUD operations, budget management, database operations
- **`goal_tracker.py`**: Savings goals management, progress tracking, goal analytics
- **`reports.py`**: Chart generation, report creation, data visualization
- **`utils.py`**: Validation, formatting, date handling, common utilities

## 📝 Contribution Guidelines

### Types of Contributions

We welcome various types of contributions:

1. **🐛 Bug Fixes**: Fix existing issues and bugs
2. **✨ New Features**: Add new functionality
3. **📚 Documentation**: Improve documentation and examples
4. **🧪 Tests**: Add or improve test coverage
5. **🎨 UI/UX**: Enhance user interface and experience
6. **⚡ Performance**: Optimize code performance
7. **🔧 Refactoring**: Improve code structure and maintainability

### Before You Start

1. **Check existing issues** to see if your idea is already being worked on
2. **Create an issue** for significant changes to discuss the approach
3. **Read the Priority TODOs** section below for high-priority items
4. **Follow the coding standards** outlined in this document

## 🎯 Priority TODOs

These are high-priority items that contributors can work on:

### 🔥 Critical Issues

1. **Fix bug: Goal progress calculation sometimes shows incorrect percentages**
   - **File**: `goal_tracker.py` (SavingsGoal class)
   - **Description**: The `progress_percentage` property may not calculate correctly in edge cases
   - **Priority**: High
   - **Estimated Effort**: 2-4 hours

2. **Add unit tests for budget and goal modules**
   - **Files**: Create `tests/test_budget.py`, `tests/test_goal_tracker.py`
   - **Description**: Add comprehensive test coverage for core functionality
   - **Priority**: High
   - **Estimated Effort**: 8-12 hours

3. **Fix budget alerts may not trigger for edge cases**
   - **File**: `budget.py` (BudgetManager class)
   - **Description**: Budget alerts may not trigger correctly for certain scenarios
   - **Priority**: High
   - **Estimated Effort**: 3-5 hours

### 🚀 New Features

4. **Add export to CSV/XLSX option**
   - **Description**: Export reports and data to CSV and Excel formats
   - **Files**: New module `export.py`, update `reports.py`
   - **Priority**: Medium
   - **Estimated Effort**: 6-8 hours
   - **Dependencies**: `openpyxl`, `pandas`

5. **Add goal completion notifications**
   - **Description**: Send email notifications when goals are completed
   - **Files**: New module `notifications.py`, update `goal_tracker.py`
   - **Priority**: Medium
   - **Estimated Effort**: 8-10 hours
   - **Dependencies**: `smtplib`, `email-validator`

6. **Add support for multiple currencies**
   - **Description**: Support different currencies for international users
   - **Files**: Update `utils.py`, `budget.py`, `goal_tracker.py`
   - **Priority**: Medium
   - **Estimated Effort**: 10-12 hours

7. **Add recurring transactions**
   - **Description**: Set up recurring income and expense entries
   - **Files**: New module `recurring.py`, update `budget.py`
   - **Priority**: Medium
   - **Estimated Effort**: 12-15 hours

8. **Add bill reminders**
   - **Description**: Set up bill payment reminders and notifications
   - **Files**: New module `reminders.py`, update `main.py`
   - **Priority**: Low
   - **Estimated Effort**: 8-10 hours

9. **Add investment tracking**
   - **Description**: Track investment portfolios and returns
   - **Files**: New module `investments.py`, update `reports.py`
   - **Priority**: Low
   - **Estimated Effort**: 15-20 hours

10. **Add bank integration**
    - **Description**: Connect with bank accounts for automatic transaction import
    - **Files**: New module `bank_integration.py`
    - **Priority**: Low
    - **Estimated Effort**: 20-25 hours
    - **Dependencies**: `requests`, `cryptography`

## 📏 Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return values
- Write **docstrings** for all functions, classes, and modules
- Use **descriptive variable names** (avoid abbreviations)
- Keep **line length** under 88 characters (Black formatter standard)

### Code Formatting

We use **Black** for code formatting:

```bash
# Format code
black budget_tracker/

# Check formatting
black --check budget_tracker/
```

### Linting

We use **flake8** for linting:

```bash
# Run linter
flake8 budget_tracker/

# Run with specific rules
flake8 --max-line-length=88 --extend-ignore=E203,W503 budget_tracker/
```

### Type Checking

We use **mypy** for type checking:

```bash
# Run type checker
mypy budget_tracker/
```

### Example Code Style

```python
def calculate_monthly_savings(income: float, expenses: float) -> float:
    """
    Calculate monthly savings from income and expenses.
    
    Args:
        income: Monthly income amount
        expenses: Monthly expenses amount
        
    Returns:
        float: Monthly savings amount
        
    Raises:
        ValueError: If income or expenses are negative
    """
    if income < 0 or expenses < 0:
        raise ValueError("Income and expenses cannot be negative")
    
    return income - expenses
```

## 🧪 Testing Guidelines

### Test Structure

Create tests in the `tests/` directory:

```
tests/
├── test_budget.py         # Tests for budget.py
├── test_goal_tracker.py   # Tests for goal_tracker.py
├── test_reports.py        # Tests for reports.py
├── test_utils.py          # Tests for utils.py
└── conftest.py            # Pytest configuration
```

### Test Naming Convention

- Test functions should start with `test_`
- Use descriptive names: `test_add_income_success`, `test_invalid_amount_raises_error`
- Group related tests in classes: `class TestBudgetManager:`

### Example Test

```python
import pytest
from budget import BudgetManager, IncomeEntry

class TestBudgetManager:
    """Test cases for BudgetManager class."""
    
    def test_add_income_success(self):
        """Test successful income addition."""
        manager = BudgetManager()
        income = IncomeEntry(
            date="2024-01-01",
            source="Salary",
            amount=50000.0,
            description="Monthly salary"
        )
        
        income_id = manager.add_income(income)
        assert income_id is not None
        assert income_id > 0
    
    def test_add_income_invalid_data(self):
        """Test income addition with invalid data."""
        manager = BudgetManager()
        income = IncomeEntry(
            date="2024-01-01",
            source="",  # Invalid empty source
            amount=50000.0,
            description="Monthly salary"
        )
        
        with pytest.raises(ValueError, match="Income source cannot be empty"):
            manager.add_income(income)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=budget_tracker --cov-report=html

# Run specific test file
pytest tests/test_budget.py

# Run with verbose output
pytest -v
```

## 🔄 Pull Request Process

### Before Submitting

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Add tests** for new functionality

4. **Update documentation** if needed

5. **Run tests and linting**:
   ```bash
   pytest
   flake8 budget_tracker/
   black --check budget_tracker/
   mypy budget_tracker/
   ```

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Template

When creating a PR, include:

- **Description**: What changes were made and why
- **Type**: Bug fix, new feature, documentation, etc.
- **Testing**: How the changes were tested
- **Screenshots**: If applicable (for UI changes)
- **Checklist**: Ensure all items are completed

### PR Checklist

- [ ] Code follows the project's coding standards
- [ ] Self-review of code has been performed
- [ ] Code has been commented, particularly in hard-to-understand areas
- [ ] Tests have been added/updated for new functionality
- [ ] Documentation has been updated if necessary
- [ ] All tests pass
- [ ] No linting errors
- [ ] Type checking passes

## 🐛 Issue Guidelines

### Bug Reports

When reporting bugs, include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the bug
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python version, etc.)
5. **Screenshots** if applicable
6. **Error messages** and stack traces

### Feature Requests

When requesting features, include:

1. **Clear title** describing the feature
2. **Use case** and motivation
3. **Proposed solution** or approach
4. **Alternatives considered**
5. **Additional context** if relevant

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `priority: high`: High priority issue
- `priority: medium`: Medium priority issue
- `priority: low`: Low priority issue

## 🚀 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality in a backwards compatible manner
- **PATCH**: Backwards compatible bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version number is updated
- [ ] CHANGELOG.md is updated
- [ ] Release notes are prepared
- [ ] Tag is created
- [ ] Release is published

## 📚 Additional Resources

### Documentation

- [Python Documentation](https://docs.python.org/3/)
- [Rich Library Documentation](https://rich.readthedocs.io/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pytest Documentation](https://docs.pytest.org/)

### Development Tools

- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Pytest Testing Framework](https://docs.pytest.org/)

## 💬 Getting Help

If you need help or have questions:

1. **Check existing issues** for similar problems
2. **Read the documentation** and code comments
3. **Create a new issue** with detailed information
4. **Join discussions** in GitHub Discussions
5. **Ask questions** in the community forum

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page
- **Project documentation**

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Thank you for contributing to the Budget Planner & Financial Goals Tracker!** 💰🎯

*Together, we can make personal finance management smarter and more accessible for everyone!*
