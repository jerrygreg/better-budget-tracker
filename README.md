# 💰 Budget Planner & Financial Goals Tracker

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-blue.svg)](https://pep8.org)

A comprehensive Python application for managing your personal finances, tracking income, expenses, budgets, and savings goals. Built with a beautiful CLI interface using the Rich library and powerful data visualization with matplotlib.

## ✨ Features

### 💰 **Income Management**
- **Income Tracking**: Record and manage all income sources
- **Multiple Sources**: Support for salary, freelance, investments, and more
- **Income Analytics**: Track income trends and patterns over time
- **Smart Validation**: Comprehensive input validation and error handling
- **Source Categorization**: Organize income by different sources

### 💸 **Expense Management**
- **Expense Tracking**: Record and categorize all expenses
- **Category Management**: Predefined and custom expense categories
- **Expense Analytics**: Analyze spending patterns and trends
- **Receipt Integration**: Add descriptions and notes to expenses
- **Date-based Filtering**: Filter expenses by date ranges

### 📊 **Budget Management**
- **Budget Limits**: Set monthly budget limits for different categories
- **Budget Monitoring**: Track spending against budget limits
- **Overspending Alerts**: Get notified when exceeding budget limits
- **Budget Analytics**: Analyze budget performance and trends
- **Flexible Categories**: Support for any expense category

### 🎯 **Savings Goals**
- **Goal Creation**: Set and track multiple savings goals
- **Progress Tracking**: Monitor progress towards financial goals
- **Goal Analytics**: Analyze goal completion rates and timelines
- **Deadline Management**: Track goal deadlines and overdue alerts
- **Goal Categories**: Organize goals by different categories

### 📈 **Reports & Analytics**
- **Rich CLI Interface**: Beautiful, colored console output with tables and panels
- **Chart Generation**: Generate charts and graphs with matplotlib
- **Comprehensive Reports**: Detailed financial summaries and analytics
- **Multiple Chart Types**: Pie charts, bar charts, histograms, and line charts
- **Export Capabilities**: Save reports and charts to files

### 🔍 **Search & Filter**
- **Advanced Search**: Find transactions by amount, category, or description
- **Smart Filtering**: Filter by date ranges, categories, and amounts
- **Flexible Sorting**: Sort by date, amount, category, or description
- **Quick Access**: Identify high-value transactions and patterns

### 🏗️ **Technical Features**
- **Data Persistence**: SQLite database for reliable data storage
- **Modular Design**: Clean, maintainable code structure with type hints
- **Error Handling**: Graceful failure modes and user-friendly error messages
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/budget-tracker.git
   cd budget-tracker
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

### Demo

Try the demo to see the application in action:

```bash
python demo.py
```

## 📖 Usage Guide

### Main Menu Navigation

The application features an intuitive CLI interface with the following main sections:

```
💰 Income Management      - Add and manage income entries
💸 Expense Management     - Add and manage expense entries
📊 Budget Management      - Set and view budget limits
🎯 Savings Goals          - Create and track savings goals
📈 Reports & Analytics    - Generate reports and charts
🔍 Search & View Data     - Search and view all data
❌ Exit                   - Close the application
```

### Adding Income

1. Select "Income Management" from the main menu
2. Choose "Add Income Entry"
3. Fill in the required information:
   - **Date**: Date of income (YYYY-MM-DD format)
   - **Source**: Income source (Salary, Freelance, Investment, etc.)
   - **Amount**: Income amount (supports various formats)
   - **Description**: Optional additional details

### Adding Expenses

1. Select "Expense Management" from the main menu
2. Choose "Add Expense Entry"
3. Fill in the required information:
   - **Date**: Date of expense (YYYY-MM-DD format)
   - **Category**: Expense category (Housing, Food, Transportation, etc.)
   - **Amount**: Expense amount (supports various formats)
   - **Description**: Optional additional details

### Setting Budgets

1. Navigate to "Budget Management"
2. Choose "Set Budget Limit"
3. Set monthly budget limits for different categories
4. Monitor spending against these limits
5. Receive alerts when approaching or exceeding budgets

### Creating Savings Goals

1. Go to "Savings Goals"
2. Choose "Create New Goal"
3. Fill in the goal details:
   - **Goal Name**: Name of the savings goal
   - **Target Amount**: Amount you want to save
   - **Target Date**: When you want to achieve the goal
   - **Category**: Goal category (Emergency Fund, Vacation, etc.)
   - **Description**: Optional additional details

### Generating Reports

1. Go to "Reports & Analytics"
2. Choose from various report types:
   - Monthly Financial Summary
   - Income vs Expenses Chart
   - Expense Breakdown by Category
   - Budget Performance Chart
   - Savings Goals Progress
   - Spending Trend Analysis
   - Comprehensive Financial Report

### Searching and Filtering

1. Access "Search & View Data"
2. Use various filtering options:
   - Search by amount, category, or description
   - Filter by date ranges
   - Show income or expenses only
   - Sort by different criteria

## 🏗️ Project Structure

```
budget_tracker/
├── main.py                 # CLI entry point with Rich library
├── budget.py               # Income, expense, and budget management
├── goal_tracker.py         # Savings goals tracking
├── reports.py              # Report generation and matplotlib charts
├── utils.py                # Validation, date parsing, and formatting
├── demo.py                 # Demo script with sample data
├── data/
│   └── budget_data.db      # SQLite database (auto-created)
├── reports/                # Generated reports and charts
├── venv/                   # Virtual environment (if created)
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── CONTRIBUTING.md        # Contribution guidelines
```

## 🔧 API Reference

### Core Classes

#### `IncomeEntry`
Data class representing an income entry.

```python
from budget import IncomeEntry

income = IncomeEntry(
    date="2024-01-01",
    source="Salary",
    amount=50000.0,
    description="Monthly salary"
)
```

#### `ExpenseEntry`
Data class representing an expense entry.

```python
from budget import ExpenseEntry

expense = ExpenseEntry(
    date="2024-01-02",
    category="Housing",
    amount=15000.0,
    description="Monthly rent"
)
```

#### `BudgetLimit`
Data class representing a budget limit.

```python
from budget import BudgetLimit

budget = BudgetLimit(
    category="Housing",
    monthly_limit=15000.0,
    description="Monthly rent budget"
)
```

#### `SavingsGoal`
Data class representing a savings goal.

```python
from goal_tracker import SavingsGoal

goal = SavingsGoal(
    name="Emergency Fund",
    target_amount=100000.0,
    current_amount=25000.0,
    target_date="2024-12-31",
    category="Emergency Fund",
    description="6 months of expenses"
)
```

#### `BudgetManager`
Manages income, expenses, and budget data.

```python
from budget import BudgetManager

manager = BudgetManager()
income_id = manager.add_income(income)
expense_id = manager.add_expense(expense)
budget_id = manager.set_budget_limit(budget)
```

#### `GoalTracker`
Manages savings goals and progress tracking.

```python
from goal_tracker import GoalTracker

tracker = GoalTracker()
goal_id = tracker.create_goal(goal)
tracker.update_goal_progress(goal_id, 5000.0)
```

#### `ReportGenerator`
Generates reports and visualizations.

```python
from reports import ReportGenerator

generator = ReportGenerator(manager, tracker)
generator.generate_monthly_summary(2024, 1)
generator.generate_income_vs_expenses_chart(2024, 1)
```

### Utility Functions

```python
from utils import validate_amount, parse_amount, format_currency

# Validate amount input
is_valid = validate_amount("1000.50")  # True

# Parse amount string
amount = parse_amount("₹1,000.50")  # 1000.5

# Format currency
formatted = format_currency(1000.5)  # "₹1,000.50"
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=budget_tracker
```

### Test Structure

```
tests/
├── test_budget.py         # Tests for budget module
├── test_goal_tracker.py   # Tests for goal tracker module
├── test_utils.py          # Tests for utility functions
└── test_reports.py        # Tests for report generation
```

## 🐛 Troubleshooting

### Common Issues

#### Database Not Found
The application automatically creates the database on first run. If you encounter issues:
```bash
# Ensure the data directory exists
mkdir -p data
```

#### Permission Errors
Make sure you have write permissions for the `data/` and `reports/` directories:
```bash
chmod 755 data reports
```

#### Chart Generation Fails
Ensure matplotlib is properly installed:
```bash
pip install --upgrade matplotlib
```

#### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Error Messages

| Error | Solution |
|-------|----------|
| `Invalid amount format` | Use supported formats like `1000.50`, `₹1,000.50`, or `$1000.50` |
| `Invalid date format` | Use YYYY-MM-DD format like `2024-01-15` |
| `Database error` | Check file permissions and disk space |
| `No data available` | Add some transactions first before generating reports |

## 🔮 Roadmap

### Planned Features

- [ ] **Excel/PDF Export**: Export reports to Excel and PDF formats
- [ ] **Email Notifications**: Send goal completion and budget alerts via email
- [ ] **Mobile App**: Cross-platform mobile support
- [ ] **Bank Integration**: Connect with bank accounts for automatic transaction import
- [ ] **Investment Tracking**: Track investment portfolios and returns
- [ ] **Bill Reminders**: Set up bill payment reminders
- [ ] **Family Sharing**: Share budgets and goals with family members
- [ ] **Recurring Transactions**: Set up recurring income and expense entries

### Known Issues

- [ ] Goal progress calculation sometimes shows incorrect percentages
- [ ] Budget alerts may not trigger for edge cases
- [ ] No support for multiple currencies yet
- [ ] Limited chart customization options

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) for the beautiful CLI interface
- [Matplotlib](https://matplotlib.org/) for data visualization
- [SQLite](https://www.sqlite.org/) for data persistence
- The Python community for excellent libraries and tools

## 📞 Support

- **Documentation**: Check this README and inline code documentation
- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/yourusername/budget-tracker/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/yourusername/budget-tracker/discussions)

## 📊 Project Statistics

- **Lines of Code**: ~3,000+
- **Test Coverage**: 85%+ (target)
- **Dependencies**: 3 core, 6 optional
- **Python Version**: 3.8+
- **Database**: SQLite
- **UI Framework**: Rich (CLI)

---

**Made with ❤️ for financial success**

*Start tracking your finances and achieving your goals today!* 💰🎯