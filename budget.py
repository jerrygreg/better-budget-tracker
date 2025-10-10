"""
Budget management module for income, expenses, and budget calculations.

This module handles all budget-related data operations including
income/expense tracking, budget limits, and financial calculations.
"""

import sqlite3
import os
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from utils import validate_amount, validate_date, format_currency, get_current_date_string


@dataclass
class IncomeEntry:
    """Data class representing an income entry."""
    id: Optional[int] = None
    date: str = ""
    source: str = ""
    amount: float = 0.0
    description: str = ""

    def __post_init__(self):
        """Validate data after initialization."""
        if self.amount < 0:
            raise ValueError("Income amount cannot be negative")
        if not self.source.strip():
            raise ValueError("Income source cannot be empty")


@dataclass
class ExpenseEntry:
    """Data class representing an expense entry."""
    id: Optional[int] = None
    date: str = ""
    category: str = ""
    amount: float = 0.0
    description: str = ""

    def __post_init__(self):
        """Validate data after initialization."""
        if self.amount < 0:
            raise ValueError("Expense amount cannot be negative")
        if not self.category.strip():
            raise ValueError("Expense category cannot be empty")


@dataclass
class BudgetLimit:
    """Data class representing a budget limit for a category."""
    id: Optional[int] = None
    category: str = ""
    monthly_limit: float = 0.0
    description: str = ""

    def __post_init__(self):
        """Validate data after initialization."""
        if self.monthly_limit < 0:
            raise ValueError("Budget limit cannot be negative")
        if not self.category.strip():
            raise ValueError("Budget category cannot be empty")


class BudgetManager:
    """Manages budget data and database operations."""
    
    def __init__(self, db_path: str = "data/budget_data.db"):
        """Initialize the budget manager with database path."""
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self) -> None:
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Income table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    source TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Expenses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Budget limits table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budget_limits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL UNIQUE,
                    monthly_limit REAL NOT NULL,
                    description TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    # Income operations
    def add_income(self, income: IncomeEntry) -> int:
        """
        Add a new income entry to the database.
        
        Args:
            income: IncomeEntry object to add
            
        Returns:
            int: ID of the created income entry
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO income (date, source, amount, description)
                    VALUES (?, ?, ?, ?)
                """, (income.date, income.source, income.amount, income.description))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")
    
    def get_all_income(self) -> List[IncomeEntry]:
        """Get all income entries."""
        income_entries = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM income ORDER BY date DESC, created_at DESC")
                rows = cursor.fetchall()
                
                for row in rows:
                    income = IncomeEntry(
                        id=row[0],
                        date=row[1],
                        source=row[2],
                        amount=row[3],
                        description=row[4] or ""
                    )
                    income_entries.append(income)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return income_entries
    
    def get_income_by_date_range(self, start_date: str, end_date: str) -> List[IncomeEntry]:
        """Get income entries within a date range."""
        income_entries = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM income 
                    WHERE date >= ? AND date <= ? 
                    ORDER BY date DESC, created_at DESC
                """, (start_date, end_date))
                rows = cursor.fetchall()
                
                for row in rows:
                    income = IncomeEntry(
                        id=row[0],
                        date=row[1],
                        source=row[2],
                        amount=row[3],
                        description=row[4] or ""
                    )
                    income_entries.append(income)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return income_entries
    
    def get_total_income_by_month(self, year: int, month: int) -> float:
        """Calculate total income for a specific month."""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        income_entries = self.get_income_by_date_range(start_date, end_date)
        return sum(income.amount for income in income_entries)
    
    # Expense operations
    def add_expense(self, expense: ExpenseEntry) -> int:
        """
        Add a new expense entry to the database.
        
        Args:
            expense: ExpenseEntry object to add
            
        Returns:
            int: ID of the created expense entry
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO expenses (date, category, amount, description)
                    VALUES (?, ?, ?, ?)
                """, (expense.date, expense.category, expense.amount, expense.description))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")
    
    def get_all_expenses(self) -> List[ExpenseEntry]:
        """Get all expense entries."""
        expense_entries = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM expenses ORDER BY date DESC, created_at DESC")
                rows = cursor.fetchall()
                
                for row in rows:
                    expense = ExpenseEntry(
                        id=row[0],
                        date=row[1],
                        category=row[2],
                        amount=row[3],
                        description=row[4] or ""
                    )
                    expense_entries.append(expense)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return expense_entries
    
    def get_expenses_by_category(self, category: str) -> List[ExpenseEntry]:
        """Get all expenses in a specific category."""
        expense_entries = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM expenses WHERE category = ? ORDER BY date DESC", (category,))
                rows = cursor.fetchall()
                
                for row in rows:
                    expense = ExpenseEntry(
                        id=row[0],
                        date=row[1],
                        category=row[2],
                        amount=row[3],
                        description=row[4] or ""
                    )
                    expense_entries.append(expense)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return expense_entries
    
    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[ExpenseEntry]:
        """Get expense entries within a date range."""
        expense_entries = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM expenses 
                    WHERE date >= ? AND date <= ? 
                    ORDER BY date DESC, created_at DESC
                """, (start_date, end_date))
                rows = cursor.fetchall()
                
                for row in rows:
                    expense = ExpenseEntry(
                        id=row[0],
                        date=row[1],
                        category=row[2],
                        amount=row[3],
                        description=row[4] or ""
                    )
                    expense_entries.append(expense)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return expense_entries
    
    def get_total_expenses_by_month(self, year: int, month: int) -> float:
        """Calculate total expenses for a specific month."""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        expense_entries = self.get_expenses_by_date_range(start_date, end_date)
        return sum(expense.amount for expense in expense_entries)
    
    def get_expenses_by_category_and_month(self, category: str, year: int, month: int) -> float:
        """Calculate total expenses for a specific category in a month."""
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
        
        expense_entries = self.get_expenses_by_date_range(start_date, end_date)
        return sum(expense.amount for expense in expense_entries if expense.category == category)
    
    # Budget limit operations
    def set_budget_limit(self, budget_limit: BudgetLimit) -> int:
        """
        Set or update a budget limit for a category.
        
        Args:
            budget_limit: BudgetLimit object
            
        Returns:
            int: ID of the created/updated budget limit
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO budget_limits (category, monthly_limit, description)
                    VALUES (?, ?, ?)
                """, (budget_limit.category, budget_limit.monthly_limit, budget_limit.description))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")
    
    def get_all_budget_limits(self) -> List[BudgetLimit]:
        """Get all budget limits."""
        budget_limits = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM budget_limits ORDER BY category")
                rows = cursor.fetchall()
                
                for row in rows:
                    budget_limit = BudgetLimit(
                        id=row[0],
                        category=row[1],
                        monthly_limit=row[2],
                        description=row[3] or ""
                    )
                    budget_limits.append(budget_limit)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return budget_limits
    
    def get_budget_limit(self, category: str) -> Optional[BudgetLimit]:
        """Get budget limit for a specific category."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM budget_limits WHERE category = ?", (category,))
                row = cursor.fetchone()
                
                if row:
                    return BudgetLimit(
                        id=row[0],
                        category=row[1],
                        monthly_limit=row[2],
                        description=row[3] or ""
                    )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return None
    
    def delete_budget_limit(self, category: str) -> bool:
        """Delete a budget limit for a category."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM budget_limits WHERE category = ?", (category,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    # Budget analysis methods
    def get_budget_status(self, year: int, month: int) -> Dict[str, Dict]:
        """
        Get budget status for a specific month.
        
        Returns:
            Dict with category status information
        """
        budget_limits = self.get_all_budget_limits()
        budget_status = {}
        
        for budget_limit in budget_limits:
            spent = self.get_expenses_by_category_and_month(budget_limit.category, year, month)
            remaining = budget_limit.monthly_limit - spent
            percentage_used = (spent / budget_limit.monthly_limit * 100) if budget_limit.monthly_limit > 0 else 0
            
            budget_status[budget_limit.category] = {
                'limit': budget_limit.monthly_limit,
                'spent': spent,
                'remaining': remaining,
                'percentage_used': percentage_used,
                'is_over_budget': spent > budget_limit.monthly_limit
            }
        
        return budget_status
    
    def get_monthly_summary(self, year: int, month: int) -> Dict[str, float]:
        """Get monthly financial summary."""
        total_income = self.get_total_income_by_month(year, month)
        total_expenses = self.get_total_expenses_by_month(year, month)
        net_income = total_income - total_expenses
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_income': net_income,
            'savings_rate': (net_income / total_income * 100) if total_income > 0 else 0
        }
    
    def get_category_summary(self, year: int, month: int) -> Dict[str, float]:
        """Get spending summary by category for a month."""
        expense_entries = self.get_expenses_by_date_range(
            f"{year}-{month:02d}-01",
            f"{year}-{month + 1:02d}-01" if month < 12 else f"{year + 1}-01-01"
        )
        
        category_totals = {}
        for expense in expense_entries:
            if expense.category not in category_totals:
                category_totals[expense.category] = 0
            category_totals[expense.category] += expense.amount
        
        return category_totals
    
    def get_overspending_alerts(self, year: int, month: int) -> List[Dict[str, any]]:
        """Get list of categories that are over budget."""
        budget_status = self.get_budget_status(year, month)
        alerts = []
        
        for category, status in budget_status.items():
            if status['is_over_budget']:
                overspent_amount = status['spent'] - status['limit']
                alerts.append({
                    'category': category,
                    'limit': status['limit'],
                    'spent': status['spent'],
                    'overspent': overspent_amount,
                    'percentage_over': (overspent_amount / status['limit'] * 100) if status['limit'] > 0 else 0
                })
        
        return alerts
    
    def search_entries(self, query: str) -> Tuple[List[IncomeEntry], List[ExpenseEntry]]:
        """Search income and expense entries by description or source/category."""
        query_lower = query.lower()
        matching_income = []
        matching_expenses = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Search income
                cursor.execute("""
                    SELECT * FROM income 
                    WHERE LOWER(source) LIKE ? OR LOWER(description) LIKE ?
                    ORDER BY date DESC
                """, (f"%{query_lower}%", f"%{query_lower}%"))
                income_rows = cursor.fetchall()
                
                for row in income_rows:
                    income = IncomeEntry(
                        id=row[0],
                        date=row[1],
                        source=row[2],
                        amount=row[3],
                        description=row[4] or ""
                    )
                    matching_income.append(income)
                
                # Search expenses
                cursor.execute("""
                    SELECT * FROM expenses 
                    WHERE LOWER(category) LIKE ? OR LOWER(description) LIKE ?
                    ORDER BY date DESC
                """, (f"%{query_lower}%", f"%{query_lower}%"))
                expense_rows = cursor.fetchall()
                
                for row in expense_rows:
                    expense = ExpenseEntry(
                        id=row[0],
                        date=row[1],
                        category=row[2],
                        amount=row[3],
                        description=row[4] or ""
                    )
                    matching_expenses.append(expense)
                    
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return matching_income, matching_expenses


# TODO: Add multi-month comparison charts for spending trends
# TODO: Add category heatmaps in reports
# TODO: Add goal completion notifications (console or email)
# TODO: Fix bug: totals sometimes miscalculate if income added before budget setup
# TODO: Add export to CSV/XLSX option
# TODO: Add dark mode support for charts
# TODO: Implement unit tests for budget and goal modules
