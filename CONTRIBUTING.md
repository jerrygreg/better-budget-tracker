# 🤝 Contributing to Budget Planner & Financial Goals Tracker

Thank you for your interest in contributing! This guide will help you get started.

## 📜 Code of Conduct

Please be respectful, inclusive, and helpful to other contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- GitHub account

### Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/budget-tracker.git
   cd budget-tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the installation**:
   ```bash
   python main.py
   python demo.py
   ```

## 📁 Project Structure

```
budget_tracker/
├── main.py                 # Main application
├── budget.py               # Income, expense, and budget management
├── goal_tracker.py         # Savings goals tracking
├── reports.py              # Report generation and charts
├── utils.py                # Utility functions
├── demo.py                 # Demo script
├── data/                   # Database storage
├── reports/                # Generated reports
└── requirements.txt        # Dependencies
```

## 📝 How to Contribute

### Types of Contributions
- **🐛 Bug Fixes**: Fix existing issues
- **✨ New Features**: Add new functionality
- **📚 Documentation**: Improve documentation
- **🎨 UI/UX**: Enhance user interface

### Before You Start
1. Check existing issues to avoid duplicates
2. Create an issue for significant changes
3. Look at the Priority TODOs below


## 📏 Coding Standards

### Python Style Guide

- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return values
- Write **docstrings** for all functions, classes, and modules
- Use **descriptive variable names** (avoid abbreviations)
- Keep **line length** under 88 characters (Black formatter standard)




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

## 📚 Additional Resources

### Documentation

- [Python Documentation](https://docs.python.org/3/)
- [Rich Library Documentation](https://rich.readthedocs.io/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Pytest Documentation](https://docs.pytest.org/)

## 💬 Getting Help

If you need help or have questions:

1. **Check existing issues** for similar problems
2. **Read the documentation** and code comments
3. **Create a new issue** with detailed information
4. **Join discussions** in GitHub Discussions

---

**Thank you for contributing to the Budget Planner & Financial Goals Tracker!** 💰🎯

*Together, we can make personal finance management smarter and more accessible for everyone!*
