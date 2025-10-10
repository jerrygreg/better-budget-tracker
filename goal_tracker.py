"""
Financial goals tracking module.

This module handles savings goals, progress tracking, and goal management.
"""

import sqlite3
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from utils import validate_amount, validate_date, format_currency, get_current_date_string


@dataclass
class SavingsGoal:
    """Data class representing a savings goal."""
    id: Optional[int] = None
    name: str = ""
    target_amount: float = 0.0
    current_amount: float = 0.0
    target_date: str = ""
    category: str = ""
    description: str = ""
    is_completed: bool = False
    created_date: str = ""

    def __post_init__(self):
        """Validate data after initialization."""
        if self.target_amount <= 0:
            raise ValueError("Target amount must be positive")
        if self.current_amount < 0:
            raise ValueError("Current amount cannot be negative")
        if not self.name.strip():
            raise ValueError("Goal name cannot be empty")
        if not validate_date(self.target_date):
            raise ValueError("Invalid target date format")
        if not validate_date(self.created_date):
            raise ValueError("Invalid created date format")

    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage."""
        if self.target_amount == 0:
            return 0.0
        return min((self.current_amount / self.target_amount) * 100, 100.0)

    @property
    def remaining_amount(self) -> float:
        """Calculate remaining amount to reach goal."""
        return max(self.target_amount - self.current_amount, 0.0)

    @property
    def days_remaining(self) -> int:
        """Calculate days remaining until target date."""
        try:
            target = datetime.strptime(self.target_date, '%Y-%m-%d').date()
            today = date.today()
            return max((target - today).days, 0)
        except ValueError:
            return 0

    @property
    def is_overdue(self) -> bool:
        """Check if goal is overdue."""
        try:
            target = datetime.strptime(self.target_date, '%Y-%m-%d').date()
            return date.today() > target and not self.is_completed
        except ValueError:
            return False


class GoalTracker:
    """Manages savings goals and progress tracking."""
    
    def __init__(self, db_path: str = "data/budget_data.db"):
        """Initialize the goal tracker with database path."""
        self.db_path = db_path
        self._ensure_data_directory()
        self._init_database()
    
    def _ensure_data_directory(self) -> None:
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def _init_database(self) -> None:
        """Initialize the SQLite database with goals table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS savings_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    target_amount REAL NOT NULL,
                    current_amount REAL DEFAULT 0.0,
                    target_date TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    is_completed BOOLEAN DEFAULT FALSE,
                    created_date TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def add_goal(self, goal: SavingsGoal) -> int:
        """
        Add a new savings goal.
        
        Args:
            goal: SavingsGoal object to add
            
        Returns:
            int: ID of the created goal
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO savings_goals 
                    (name, target_amount, current_amount, target_date, category, description, is_completed, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    goal.name,
                    goal.target_amount,
                    goal.current_amount,
                    goal.target_date,
                    goal.category,
                    goal.description,
                    goal.is_completed,
                    goal.created_date
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise ValueError(f"Database error: {e}")
    
    def get_all_goals(self) -> List[SavingsGoal]:
        """Get all savings goals."""
        goals = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM savings_goals ORDER BY target_date ASC, created_at DESC")
                rows = cursor.fetchall()
                
                for row in rows:
                    goal = SavingsGoal(
                        id=row[0],
                        name=row[1],
                        target_amount=row[2],
                        current_amount=row[3],
                        target_date=row[4],
                        category=row[5],
                        description=row[6] or "",
                        is_completed=bool(row[7]),
                        created_date=row[8]
                    )
                    goals.append(goal)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return goals
    
    def get_goal_by_id(self, goal_id: int) -> Optional[SavingsGoal]:
        """Get a specific goal by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM savings_goals WHERE id = ?", (goal_id,))
                row = cursor.fetchone()
                
                if row:
                    return SavingsGoal(
                        id=row[0],
                        name=row[1],
                        target_amount=row[2],
                        current_amount=row[3],
                        target_date=row[4],
                        category=row[5],
                        description=row[6] or "",
                        is_completed=bool(row[7]),
                        created_date=row[8]
                    )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return None
    
    def update_goal(self, goal: SavingsGoal) -> bool:
        """
        Update an existing goal.
        
        Args:
            goal: SavingsGoal object with updated data
            
        Returns:
            bool: True if update was successful
        """
        if not goal.id:
            raise ValueError("Goal ID is required for update")
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE savings_goals 
                    SET name = ?, target_amount = ?, current_amount = ?, 
                        target_date = ?, category = ?, description = ?, is_completed = ?
                    WHERE id = ?
                """, (
                    goal.name,
                    goal.target_amount,
                    goal.current_amount,
                    goal.target_date,
                    goal.category,
                    goal.description,
                    goal.is_completed,
                    goal.id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def delete_goal(self, goal_id: int) -> bool:
        """Delete a goal by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM savings_goals WHERE id = ?", (goal_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def add_progress(self, goal_id: int, amount: float) -> bool:
        """
        Add progress to a goal.
        
        Args:
            goal_id: ID of the goal
            amount: Amount to add to current progress
            
        Returns:
            bool: True if successful
        """
        if amount <= 0:
            raise ValueError("Progress amount must be positive")
        
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            raise ValueError("Goal not found")
        
        goal.current_amount += amount
        
        # Check if goal is completed
        if goal.current_amount >= goal.target_amount:
            goal.is_completed = True
            goal.current_amount = goal.target_amount  # Cap at target amount
        
        return self.update_goal(goal)
    
    def get_goals_by_category(self, category: str) -> List[SavingsGoal]:
        """Get all goals in a specific category."""
        goals = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM savings_goals WHERE category = ? ORDER BY target_date ASC", (category,))
                rows = cursor.fetchall()
                
                for row in rows:
                    goal = SavingsGoal(
                        id=row[0],
                        name=row[1],
                        target_amount=row[2],
                        current_amount=row[3],
                        target_date=row[4],
                        category=row[5],
                        description=row[6] or "",
                        is_completed=bool(row[7]),
                        created_date=row[8]
                    )
                    goals.append(goal)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return goals
    
    def get_active_goals(self) -> List[SavingsGoal]:
        """Get all active (non-completed) goals."""
        all_goals = self.get_all_goals()
        return [goal for goal in all_goals if not goal.is_completed]
    
    def get_completed_goals(self) -> List[SavingsGoal]:
        """Get all completed goals."""
        all_goals = self.get_all_goals()
        return [goal for goal in all_goals if goal.is_completed]
    
    def get_overdue_goals(self) -> List[SavingsGoal]:
        """Get all overdue goals."""
        all_goals = self.get_all_goals()
        return [goal for goal in all_goals if goal.is_overdue]
    
    def get_goals_summary(self) -> Dict[str, any]:
        """Get summary statistics for all goals."""
        all_goals = self.get_all_goals()
        active_goals = self.get_active_goals()
        completed_goals = self.get_completed_goals()
        overdue_goals = self.get_overdue_goals()
        
        total_target_amount = sum(goal.target_amount for goal in all_goals)
        total_current_amount = sum(goal.current_amount for goal in all_goals)
        total_remaining = sum(goal.remaining_amount for goal in active_goals)
        
        return {
            'total_goals': len(all_goals),
            'active_goals': len(active_goals),
            'completed_goals': len(completed_goals),
            'overdue_goals': len(overdue_goals),
            'total_target_amount': total_target_amount,
            'total_current_amount': total_current_amount,
            'total_remaining': total_remaining,
            'overall_progress': (total_current_amount / total_target_amount * 100) if total_target_amount > 0 else 0
        }
    
    def get_category_summary(self) -> Dict[str, Dict[str, float]]:
        """Get summary statistics by category."""
        all_goals = self.get_all_goals()
        category_data = {}
        
        for goal in all_goals:
            if goal.category not in category_data:
                category_data[goal.category] = {
                    'total_goals': 0,
                    'active_goals': 0,
                    'completed_goals': 0,
                    'total_target': 0.0,
                    'total_current': 0.0,
                    'total_remaining': 0.0
                }
            
            category_data[goal.category]['total_goals'] += 1
            category_data[goal.category]['total_target'] += goal.target_amount
            category_data[goal.category]['total_current'] += goal.current_amount
            
            if goal.is_completed:
                category_data[goal.category]['completed_goals'] += 1
            else:
                category_data[goal.category]['active_goals'] += 1
                category_data[goal.category]['total_remaining'] += goal.remaining_amount
        
        # Calculate percentages
        for category in category_data:
            data = category_data[category]
            if data['total_target'] > 0:
                data['progress_percentage'] = (data['total_current'] / data['total_target']) * 100
            else:
                data['progress_percentage'] = 0.0
        
        return category_data
    
    def search_goals(self, query: str) -> List[SavingsGoal]:
        """Search goals by name, category, or description."""
        query_lower = query.lower()
        matching_goals = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM savings_goals 
                    WHERE LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(description) LIKE ?
                    ORDER BY target_date ASC
                """, (f"%{query_lower}%", f"%{query_lower}%", f"%{query_lower}%"))
                rows = cursor.fetchall()
                
                for row in rows:
                    goal = SavingsGoal(
                        id=row[0],
                        name=row[1],
                        target_amount=row[2],
                        current_amount=row[3],
                        target_date=row[4],
                        category=row[5],
                        description=row[6] or "",
                        is_completed=bool(row[7]),
                        created_date=row[8]
                    )
                    matching_goals.append(goal)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        
        return matching_goals
    
    def get_goals_due_soon(self, days: int = 30) -> List[SavingsGoal]:
        """Get goals that are due within the specified number of days."""
        all_goals = self.get_active_goals()
        due_soon = []
        
        for goal in all_goals:
            if goal.days_remaining <= days:
                due_soon.append(goal)
        
        return sorted(due_soon, key=lambda g: g.days_remaining)
    
    def get_goals_progress_trend(self, goal_id: int, months: int = 6) -> List[Dict[str, any]]:
        """
        Get progress trend for a goal over time.
        Note: This is a simplified version. In a real app, you'd track progress history.
        """
        goal = self.get_goal_by_id(goal_id)
        if not goal:
            return []
        
        # For demo purposes, create mock progress data
        trend_data = []
        current_date = date.today()
        
        for i in range(months):
            month_date = current_date - timedelta(days=30 * i)
            # Mock progress calculation (in real app, this would come from historical data)
            progress_amount = goal.current_amount * (1 - (i * 0.1))  # Decreasing progress going back in time
            progress_amount = max(progress_amount, 0)
            
            trend_data.append({
                'date': month_date.strftime('%Y-%m-%d'),
                'amount': progress_amount,
                'percentage': (progress_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
            })
        
        return list(reversed(trend_data))  # Return in chronological order


# TODO: Add multi-month comparison charts for spending trends
# TODO: Add category heatmaps in reports
# TODO: Add goal completion notifications (console or email)
# TODO: Fix bug: totals sometimes miscalculate if income added before budget setup
# TODO: Add export to CSV/XLSX option
# TODO: Add dark mode support for charts
# TODO: Implement unit tests for budget and goal modules
