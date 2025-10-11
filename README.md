# 💰 Budget Planner & Financial Goals Tracker

A comprehensive Python application for managing your personal finances. Track income, expenses, budgets, and savings goals with a beautiful command-line interface using the Rich library and powerful data visualization with matplotlib.

## ✨ Features

### 💰 **Income Management**
- **Income Tracking**: Record and manage all income sources
- **Multiple Sources**: Support for salary, freelance, investments, and more
- **Income Analytics**: Track income trends and patterns over time
- **Source Categorization**: Organize income by different sources

### 💸 **Expense Management**
- **Expense Tracking**: Record and categorize all expenses
- **Category Management**: Predefined and custom expense categories
- **Expense Analytics**: Analyze spending patterns and trends
- **Date-based Filtering**: Filter expenses by date ranges

### 📊 **Budget Management**
- **Budget Limits**: Set monthly budget limits for different categories
- **Budget Monitoring**: Track spending against budget limits
- **Overspending Alerts**: Get notified when exceeding budget limits
- **Budget Analytics**: Analyze budget performance and trends

### 🎯 **Savings Goals**
- **Goal Creation**: Set and track multiple savings goals
- **Progress Tracking**: Monitor progress towards financial goals
- **Goal Analytics**: Analyze goal completion rates and timelines
- **Deadline Management**: Track goal deadlines and overdue alerts

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

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- GitHub account

### Installation

1. **Fork the repository**:
   - Go to [https://github.com/debugfest/budget-tracker](https://github.com/debugfest/budget-tracker)
   - Click the "Fork" button in the top-right corner
   - This creates your own copy of the repository

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/budget-tracker.git
   cd budget-tracker
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

### First Time Setup
1. The application will automatically create a database in the `data/` folder
2. Start by adding some income and expenses
3. Set up your budget limits
4. Create your first savings goal

## 📖 How to Use

The application has a simple menu-driven interface:

```
💰 Income Management      - Add and manage income
💸 Expense Management     - Add and manage expenses  
📊 Budget Management      - Set budget limits
🎯 Savings Goals          - Create savings goals
📈 Reports & Analytics    - View reports and charts
🔍 Search & View Data     - Search transactions
❌ Exit                   - Close application
```

### Quick Start Guide
1. **Add Income**: Go to Income Management → Add Income Entry
2. **Add Expenses**: Go to Expense Management → Add Expense Entry  
3. **Set Budgets**: Go to Budget Management → Set Budget Limit
4. **Create Goals**: Go to Savings Goals → Create New Goal
5. **View Reports**: Go to Reports & Analytics → Choose report type

### Input Format
- **Date**: Use YYYY-MM-DD format (e.g., 2024-01-15)
- **Amount**: Enter numbers (e.g., 1000.50 or ₹1,000.50)
- **Categories**: Use predefined categories or create custom ones

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
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── CONTRIBUTING.md        # Contribution guidelines
```

## 🔧 API Reference

### Core Classes

#### `BudgetManager`
Manages income, expenses, and budget data.

```python
from budget import BudgetManager, IncomeEntry, ExpenseEntry

manager = BudgetManager()

# Add income
income = IncomeEntry(
    date="2024-01-01",
    source="Salary",
    amount=50000.0,
    description="Monthly salary"
)
income_id = manager.add_income(income)

# Add expense
expense = ExpenseEntry(
    date="2024-01-02",
    category="Housing",
    amount=15000.0,
    description="Monthly rent"
)
expense_id = manager.add_expense(expense)
```

#### `GoalTracker`
Manages savings goals and progress tracking.

```python
from goal_tracker import GoalTracker, SavingsGoal

tracker = GoalTracker()

goal = SavingsGoal(
    name="Emergency Fund",
    target_amount=100000.0,
    current_amount=25000.0,
    target_date="2024-12-31",
    category="Emergency Fund",
    description="6 months of expenses"
)
goal_id = tracker.create_goal(goal)
```

#### `ReportGenerator`
Generates reports and visualizations.

```python
from reports import ReportGenerator

generator = ReportGenerator(manager, tracker)
generator.generate_monthly_summary(2024, 1)
generator.generate_income_vs_expenses_chart(2024, 1)
```

## 🐛 Troubleshooting

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


## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) for the beautiful CLI interface
- [Matplotlib](https://matplotlib.org/) for data visualization
- [SQLite](https://www.sqlite.org/) for data persistence
- The Python community for excellent libraries and tools

---

**Made with ❤️ for financial success**

*Start tracking your finances and achieving your goals today!* 💰🎯