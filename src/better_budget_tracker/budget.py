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

from better_budget_tracker.utils import validate_amount, validate_date, format_currency, get_current_date_string


@dataclass
class IncomeEntry:
    """
    Data class representing an income entry.

    Attributes:
        id: The ID of the income entry.
        date: The date the income entry was created.
        source: The source of the income entry.
        amount: The amount of the income entry.
        description: The description of the income entry.
        alias: The alias of the source, if an alias was used
    """
    id: Optional[int] = None
    date: str = ""
    source: str = ""
    amount: float = 0.0
    description: str = ""
    alias: Optional[str] = None

    def __post_init__(self):
        """Validate data after initialization."""
        if self.amount < 0:
            raise ValueError("Income amount cannot be negative")
        if not self.source.strip():
            raise ValueError("Income source cannot be empty")


@dataclass
class AliasEntry:
    """
    Data class representing a category/source alias.

    Attributes:
        id: The ID of the alias entry.
        alias: The alias.
        full_name: The full name of the alias.
        type: The table this is associated with.
    """
    id: Optional[int] = None
    alias: str = ""
    full_name: str = ""
    type: str = ""  # 'income' or 'expense'

    def __post_init__(self):
        """Validate data after initialization."""
        if not self.alias.strip():
            raise ValueError("Alias cannot be empty")
        elif not self.full_name.strip():
            raise ValueError("Full name cannot be empty")
        if self.type not in ['income', 'expenses']:
            raise ValueError("Alias type must be 'income' or 'expenses'")


@dataclass
class ExpenseEntry:
    """Data class representing an expense entry."""
    id: Optional[int] = None
    date: str = ""
    category: str = ""
    amount: float = 0.0
    description: str = ""
    alias: Optional[str] = None

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
                CREATE TABLE IF NOT EXISTS \"income\" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    source TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT DEFAULT '',
                    alias TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Aliases table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS \"aliases\" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alias TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (alias, type)
                )
            """)
            
            # Expenses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS \"expenses\" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT DEFAULT '',
                    alias TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Budget limits table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS \"budget_limits\" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL UNIQUE,
                    monthly_limit REAL NOT NULL,
                    description TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()

    def reindex_table(self, table_name: str) -> bool:
        """
        Re-indexes the primary key for a given table to be sequential from 1.

        ⚠️ WARNING: This is a destructive operation. It should not be used on
        tables that are referenced by foreign keys in other tables.

        Args:
            table_name: The name of the table to re-index (e.g., 'income').

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        temp_table_name = f"{table_name}_temp"

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Start a transaction
                cursor.execute("BEGIN TRANSACTION;")

                # 1. Get the original table's CREATE statement
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                create_sql = cursor.fetchone()[0]

                # 2. Create the temporary table with the same schema
                temp_create_sql = create_sql.replace(f"CREATE TABLE \"{table_name}\"", f"CREATE TABLE \"{temp_table_name}\"")
                cursor.execute(temp_create_sql)

                # 3. Get column names, excluding the 'id' primary key
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall() if row[1] != 'id']
                column_str = ", ".join(columns)

                # 4. Copy data from the old table to the new one, ordered by the old id
                # The new table will auto-generate sequential IDs from 1.
                cursor.execute(f"""
                        INSERT INTO {temp_table_name} ({column_str})
                        SELECT {column_str} FROM {table_name} ORDER BY id ASC
                    """)

                # 5. Drop the original table
                cursor.execute(f"DROP TABLE {table_name}")

                # 6. Rename the temporary table to the original name
                cursor.execute(f"ALTER TABLE {temp_table_name} RENAME TO {table_name}")

                # 7. If using AUTOINCREMENT, reset the sequence counter
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")

                # Commit the transaction
                conn.commit()
                return True

        except sqlite3.Error as e:
            raise ValueError(f"Database error during re-indexing: {e}")
            # If an error occurs, the transaction will be automatically rolled back
            # by the 'with' statement context manager.

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
                    INSERT INTO income (date, source, amount, description, alias)
                    VALUES (?, ?, ?, ?, ?)
                """, (income.date, income.source, income.amount, income.description, income.alias))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")

    def delete_income(self, id_input: int) -> IncomeEntry:
        """
        Add a new income entry to the database.

        Args:
            id_input: ID of the income entry to delete

        Returns:
            IncomeEntry: The deleted income entry

        Raises:
            ValueError: If the income entry does not exist
            AssertionError: If it deletes multiple entries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Get deleted contents
                cursor.execute("""
                    SELECT * FROM income WHERE id = ?
                """, (id_input,))

                deleted_row = cursor.fetchone()

                # Delete contents
                cursor.execute("""
                    DELETE FROM income WHERE id = ?
                """, (id_input,))
                conn.commit()
                n_deleted_rows = cursor.rowcount  # will be 1 if delete works

                assert(n_deleted_rows <= 1), "Multiple rows deleted" # Should never have duplicate ids
                if n_deleted_rows == 1:
                    # return deleted entry
                    return IncomeEntry(
                        id=deleted_row[0],
                        date=deleted_row[1],
                        source=deleted_row[2],
                        amount=deleted_row[3],
                        description=deleted_row[4] or "",
                        alias=deleted_row[5] or ""
                    )
                else:
                    raise KeyError(f"Income entry with id {id_input} was not found")

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
                        description=row[4] or "",
                        alias=row[5] or None
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
                        description=row[4] or "",
                        alias=row[5] or None
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
                    INSERT INTO expenses (date, category, amount, description, alias)
                    VALUES (?, ?, ?, ?, ?)
                """, (expense.date, expense.category, expense.amount, expense.description, expense.alias))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")

    def delete_expense(self, id_input: int) -> ExpenseEntry:
        """
        Add a new income entry to the database.

        Args:
            id_input: ID of the expense entry to delete

        Returns:
            ExpenseEntry: The deleted expense entry

        Raises:
            ValueError: If the expense entry does not exist
            AssertionError: If it deletes multiple entries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Get deleted contents
                cursor.execute("""
                    SELECT * FROM expenses WHERE id = ?
                """, (id_input, ))

                deleted_row = cursor.fetchone()

                # Delete contents
                cursor.execute("""
                    DELETE FROM expenses WHERE id = ?
                """, (id_input, ))
                conn.commit()
                n_deleted_rows = cursor.rowcount  # will be 1 if delete works

                assert(n_deleted_rows <= 1), "Multiple rows deleted" # Should never have duplicate ids
                if n_deleted_rows == 1:
                    # return deleted entry
                    return ExpenseEntry(
                        id=deleted_row[0],
                        date=deleted_row[1],
                        category=deleted_row[2],
                        amount=deleted_row[3],
                        description=deleted_row[4] or "",
                        alias=deleted_row[5] or None
                    )
                else:
                    raise KeyError(f"Expense entry with id {id_input} was not found")

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
                        description=row[4] or "",
                        alias=row[5] or None
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
                        description=row[4] or "",
                        alias=row[5] or None
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
                        description=row[4] or "",
                        alias=row[5] or None
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

    # Alias operations
    def add_alias(self, alias: AliasEntry) -> int:
        """
        Add an alias entry.

        Args:
            alias: Alias entry

        Returns:
            int: ID of the created alias

        Raises:
            ValueError: SQL database error
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO aliases (alias, full_name, type) 
                    VALUES (?, ?, ?)
                """, (alias.alias, alias.full_name, alias.type))
                conn.commit()
                return cursor.lastrowid

        except sqlite3.IntegrityError:
            # This happens if the alias is not unique
            raise KeyError(f"Alias '{alias.alias}' already exists.")
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")

    def get_alias(self, alias: str, table: str) -> AliasEntry | None:
        """
        Resolve an alias entry.

        Args:
            alias: The alias to resolve
            table: The table the alias is related to 'income' or 'expenses'

        Returns:
            AliasEntry | None: The resolved alias entry, or ``None`` if the alias does not exist
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM aliases WHERE alias = ? AND type = ?
                """, (alias, table))
                alias = cursor.fetchone()

                if alias:
                    return AliasEntry(
                        id=alias[0],
                        alias=alias[1],
                        full_name=alias[2],
                        type=alias[3]
                    )
                else: # No match found
                    return None

        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")

    def get_all_aliases(self, table: str) -> List[AliasEntry]:
        """
        Get all the aliases for a specific table.
        Args:
            table: The table the alias is related to 'income' or 'expenses'

        Returns:
            List[AliasEntry]: The list of aliases for the given table

        """
        aliases = []

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                if table.lower() == "all":
                    cursor.execute("""
                        SELECT * FROM aliases
                    """)
                else:
                    cursor.execute("""
                        SELECT * FROM aliases WHERE type = ?
                    """, (table, ))

                rows = cursor.fetchall()

                for row in rows:
                    aliases.append(AliasEntry(
                        id=row[0],
                        alias=row[1],
                        full_name=row[2],
                        type=row[3]
                    ))

        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")

        return aliases

    def delete_alias(self, alias: str, table: str) -> AliasEntry:
        """
        Delete an alias entry by its ID.

        Args:
            alias: ID of the alias entry to delete
            table: The table the alias is related to 'income' or 'expenses'

        Returns:
            AliasEntry: The deleted alias entry

        Raises:
            KeyError: If the alias entry does not exist
            AssertionError: If it deletes multiple entries
            ValueError: If a database error occurs
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Get deleted contents
                cursor.execute("""
                    SELECT * FROM aliases WHERE alias = ? AND type = ?
                """, (alias, table))

                deleted_row = cursor.fetchone()

                # Delete contents
                cursor.execute("""
                    DELETE FROM aliases WHERE alias = ? AND type = ?
                """, (alias, table))
                conn.commit()
                n_deleted_rows = cursor.rowcount  # will be 1 if delete works

                assert(n_deleted_rows <= 1), "Multiple rows deleted" # Should never have duplicates
                if n_deleted_rows == 1:
                    # return deleted entry
                    return AliasEntry(
                        id=deleted_row[0],
                        alias=deleted_row[1],
                        full_name=deleted_row[2],
                        type=deleted_row[3]
                    )
                else:
                    raise KeyError(f"Alias entry for the {table} table with alias {alias} was not found")

        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")



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
                        description=row[4] or "",
                        alias=row[5] or None
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
                        description=row[4] or "",
                        alias=row[5] or None
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
