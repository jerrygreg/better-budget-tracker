"""
Report generation module for budget tracker.

This module handles generating various reports including summaries,
analytics, and visualizations using matplotlib.
"""

import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from better_budget_tracker.budget import BudgetManager, IncomeEntry, ExpenseEntry, BudgetLimit
from better_budget_tracker.goal_tracker import GoalTracker, SavingsGoal
from better_budget_tracker.utils import format_currency, format_date, format_percentage, get_month_start_date, get_month_end_date


class ReportGenerator:
    """Generates various reports and visualizations for budget tracking."""
    
    def __init__(self, budget_manager: BudgetManager, goal_tracker: GoalTracker, reports_dir: str):
        """
        Initialize the report generator.
        
        Args:
            budget_manager: BudgetManager instance
            goal_tracker: GoalTracker instance
        """
        self.budget_manager = budget_manager
        self.goal_tracker = goal_tracker
        self.reports_dir = reports_dir
        self._ensure_reports_directory(reports_dir)
    
    def _ensure_reports_directory(self, reports_dir: str) -> None:
        """Ensure the reports directory exists."""
        os.makedirs(reports_dir, exist_ok=True)
    
    def generate_monthly_summary(self, year: int, month: int, save_to_file: bool = True) -> str:
        """
        Generate a monthly financial summary report.
        
        Args:
            year: Year for the report
            month: Month for the report
            save_to_file: Whether to save the report to a file
            
        Returns:
            str: Generated report content
        """
        monthly_summary = self.budget_manager.get_monthly_summary(year, month)
        budget_status = self.budget_manager.get_budget_status(year, month)
        category_summary = self.budget_manager.get_category_summary(year, month)
        overspending_alerts = self.budget_manager.get_overspending_alerts(year, month)
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append(f"MONTHLY FINANCIAL SUMMARY - {format_date(f'{year}-{month:02d}-01', output_format='%B %Y')}")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        report_lines.append("")
        
        # Financial overview
        report_lines.append("FINANCIAL OVERVIEW")
        report_lines.append("-" * 20)
        report_lines.append(f"Total Income: {format_currency(monthly_summary['total_income'])}")
        report_lines.append(f"Total Expenses: {format_currency(monthly_summary['total_expenses'])}")
        report_lines.append(f"Net Income: {format_currency(monthly_summary['net_income'])}")
        report_lines.append(f"Savings Rate: {monthly_summary['savings_rate']:.1f}%")
        report_lines.append("")
        
        # Budget status
        if budget_status:
            report_lines.append("BUDGET STATUS")
            report_lines.append("-" * 15)
            for category, status in budget_status.items():
                status_icon = "🔴" if status['is_over_budget'] else "🟢"
                report_lines.append(f"{status_icon} {category}: {format_currency(status['spent'])} / {format_currency(status['limit'])} "
                                  f"({status['percentage_used']:.1f}%)")
                if status['remaining'] > 0:
                    report_lines.append(f"   Remaining: {format_currency(status['remaining'])}")
            report_lines.append("")
        
        # Overspending alerts
        if overspending_alerts:
            report_lines.append("OVERSPENDING ALERTS")
            report_lines.append("-" * 20)
            for alert in overspending_alerts:
                report_lines.append(f"⚠️  {alert['category']}: Over budget by {format_currency(alert['overspent'])} "
                                  f"({alert['percentage_over']:.1f}% over limit)")
            report_lines.append("")
        
        # Category breakdown
        if category_summary:
            report_lines.append("EXPENSE BREAKDOWN BY CATEGORY")
            report_lines.append("-" * 30)
            total_expenses = sum(category_summary.values())
            for category, amount in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                report_lines.append(f"{category}: {format_currency(amount)} ({percentage:.1f}%)")
        
        report_content = "\n".join(report_lines)
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/monthly_summary_{year}_{month:02d}_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write(report_content)
            print(f"Monthly summary saved to: {filename}")
        
        return report_content
    
    def generate_goals_summary(self, save_to_file: bool = True) -> str:
        """
        Generate a savings goals summary report.
        
        Args:
            save_to_file: Whether to save the report to a file
            
        Returns:
            str: Generated report content
        """
        goals_summary = self.goal_tracker.get_goals_summary()
        category_summary = self.goal_tracker.get_category_summary()
        active_goals = self.goal_tracker.get_active_goals()
        completed_goals = self.goal_tracker.get_completed_goals()
        overdue_goals = self.goal_tracker.get_overdue_goals()
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("SAVINGS GOALS SUMMARY")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        report_lines.append("")
        
        # Overall summary
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 20)
        report_lines.append(f"Total Goals: {goals_summary['total_goals']}")
        report_lines.append(f"Active Goals: {goals_summary['active_goals']}")
        report_lines.append(f"Completed Goals: {goals_summary['completed_goals']}")
        report_lines.append(f"Overdue Goals: {goals_summary['overdue_goals']}")
        report_lines.append(f"Total Target Amount: {format_currency(goals_summary['total_target_amount'])}")
        report_lines.append(f"Total Current Amount: {format_currency(goals_summary['total_current_amount'])}")
        report_lines.append(f"Total Remaining: {format_currency(goals_summary['total_remaining'])}")
        report_lines.append(f"Overall Progress: {goals_summary['overall_progress']:.1f}%")
        report_lines.append("")
        
        # Active goals
        if active_goals:
            report_lines.append("ACTIVE GOALS")
            report_lines.append("-" * 15)
            for goal in active_goals:
                status_icon = "🔴" if goal.is_overdue else "🟡"
                report_lines.append(f"{status_icon} {goal.name} ({goal.category})")
                report_lines.append(f"   Progress: {format_currency(goal.current_amount)} / {format_currency(goal.target_amount)} "
                                  f"({goal.progress_percentage:.1f}%)")
                report_lines.append(f"   Target Date: {format_date(goal.target_date)} ({goal.days_remaining} days remaining)")
                if goal.description:
                    report_lines.append(f"   Description: {goal.description}")
                report_lines.append("")
        
        # Completed goals
        if completed_goals:
            report_lines.append("COMPLETED GOALS")
            report_lines.append("-" * 17)
            for goal in completed_goals:
                report_lines.append(f"✅ {goal.name} ({goal.category})")
                report_lines.append(f"   Amount: {format_currency(goal.target_amount)}")
                report_lines.append(f"   Completed: {format_date(goal.target_date)}")
                report_lines.append("")
        
        # Category breakdown
        if category_summary:
            report_lines.append("GOALS BY CATEGORY")
            report_lines.append("-" * 20)
            for category, data in category_summary.items():
                report_lines.append(f"{category}:")
                report_lines.append(f"   Goals: {data['active_goals']} active, {data['completed_goals']} completed")
                report_lines.append(f"   Target: {format_currency(data['total_target'])}")
                report_lines.append(f"   Current: {format_currency(data['total_current'])}")
                report_lines.append(f"   Progress: {data['progress_percentage']:.1f}%")
                report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/goals_summary_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write(report_content)
            print(f"Goals summary saved to: {filename}")
        
        return report_content
    
    def generate_spending_chart(self, year: int, month: int, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a pie chart showing spending by category.
        
        Args:
            year: Year for the chart
            month: Month for the chart
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        category_summary = self.budget_manager.get_category_summary(year, month)
        
        if not category_summary:
            print("No spending data available for chart generation.")
            return None
        
        # Prepare data
        categories = list(category_summary.keys())
        amounts = list(category_summary.values())
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
        
        wedges, texts, autotexts = plt.pie(
            amounts,
            labels=categories,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        # Customize the chart
        plt.title(f'Spending by Category - {format_date(f"{year}-{month:02d}-01", output_format="%B %Y")}', 
                 fontsize=16, fontweight='bold')
        
        # Improve text readability
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        plt.axis('equal')
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/spending_chart_{year}_{month:02d}_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Spending chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_budget_status_chart(self, year: int, month: int, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a bar chart showing budget status by category.
        
        Args:
            year: Year for the chart
            month: Month for the chart
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        budget_status = self.budget_manager.get_budget_status(year, month)
        
        if not budget_status:
            print("No budget data available for chart generation.")
            return None
        
        # Prepare data
        categories = list(budget_status.keys())
        limits = [status['limit'] for status in budget_status.values()]
        spent = [status['spent'] for status in budget_status.values()]
        
        # Create bar chart
        x = np.arange(len(categories))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars1 = ax.bar(x - width/2, limits, width, label='Budget Limit', color='lightblue', alpha=0.7)
        bars2 = ax.bar(x + width/2, spent, width, label='Amount Spent', color='lightcoral', alpha=0.7)
        
        # Customize the chart
        ax.set_xlabel('Categories')
        ax.set_ylabel('Amount')
        ax.set_title(f'Budget Status - {format_date(f"{year}-{month:02d}-01", output_format="%B %Y")}')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{height:,.0f}', ha='center', va='bottom', fontsize=8)
        
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'{height:,.0f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/budget_status_{year}_{month:02d}_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Budget status chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_goals_progress_chart(self, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a bar chart showing progress for all active goals.
        
        Args:
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        active_goals = self.goal_tracker.get_active_goals()
        
        if not active_goals:
            print("No active goals available for chart generation.")
            return None
        
        # Prepare data
        goal_names = [goal.name for goal in active_goals]
        progress_percentages = [goal.progress_percentage for goal in active_goals]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        colors = ['green' if p >= 80 else 'orange' if p >= 50 else 'red' for p in progress_percentages]
        
        bars = plt.bar(range(len(goal_names)), progress_percentages, color=colors, alpha=0.7)
        
        # Customize the chart
        plt.title('Savings Goals Progress', fontsize=16, fontweight='bold')
        plt.xlabel('Goals')
        plt.ylabel('Progress (%)')
        plt.xticks(range(len(goal_names)), goal_names, rotation=45, ha='right')
        plt.ylim(0, 100)
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, percentage in zip(bars, progress_percentages):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{percentage:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/goals_progress_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Goals progress chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_income_vs_expenses_chart(self, year: int, month: int, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a chart comparing income vs expenses.
        
        Args:
            year: Year for the chart
            month: Month for the chart
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        monthly_summary = self.budget_manager.get_monthly_summary(year, month)
        
        if monthly_summary['total_income'] == 0 and monthly_summary['total_expenses'] == 0:
            print("No financial data available for chart generation.")
            return None
        
        # Prepare data
        categories = ['Income', 'Expenses']
        amounts = [monthly_summary['total_income'], monthly_summary['total_expenses']]
        colors = ['green', 'red']
        
        # Create bar chart
        plt.figure(figsize=(8, 6))
        bars = plt.bar(categories, amounts, color=colors, alpha=0.7)
        
        # Customize the chart
        plt.title(f'Income vs Expenses - {format_date(f"{year}-{month:02d}-01", output_format="%B %Y")}', 
                 fontsize=16, fontweight='bold')
        plt.ylabel('Amount')
        plt.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, amount in zip(bars, amounts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + amount*0.01,
                    f'{amount:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Add net income line
        net_income = monthly_summary['net_income']
        if net_income != 0:
            plt.axhline(y=net_income, color='blue', linestyle='--', alpha=0.7, 
                       label=f'Net Income: {net_income:,.0f}')
            plt.legend()
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/income_vs_expenses_{year}_{month:02d}_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Income vs expenses chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_monthly_trend_chart(self, months: int = 6, save_to_file: bool = True) -> Optional[str]:
        """
        Generate a line chart showing monthly income and expense trends.
        
        Args:
            months: Number of months to show
            save_to_file: Whether to save the chart to a file
            
        Returns:
            Optional[str]: Path to saved file if save_to_file is True
        """
        # Get data for the last N months
        end_date = date.today()
        start_date = end_date - timedelta(days=30 * months)
        
        months_data = []
        income_data = []
        expense_data = []
        
        current_date = start_date
        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            
            monthly_summary = self.budget_manager.get_monthly_summary(year, month)
            
            months_data.append(current_date)
            income_data.append(monthly_summary['total_income'])
            expense_data.append(monthly_summary['total_expenses'])
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        if not any(income_data) and not any(expense_data):
            print("No trend data available for chart generation.")
            return None
        
        # Create line chart
        plt.figure(figsize=(12, 6))
        plt.plot(months_data, income_data, marker='o', linewidth=2, label='Income', color='green')
        plt.plot(months_data, expense_data, marker='s', linewidth=2, label='Expenses', color='red')
        
        # Customize the chart
        plt.title(f'Monthly Income vs Expenses Trend - Last {months} Months', 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/monthly_trend_{months}months_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"Monthly trend chart saved to: {filename}")
            plt.close()
            return filename
        else:
            plt.show()
            return None
    
    def generate_comprehensive_report(self, year: int, month: int, save_to_file: bool = True) -> str:
        """
        Generate a comprehensive report with all available data and charts.
        
        Args:
            year: Year for the report
            month: Month for the report
            save_to_file: Whether to save the report and charts to files
            
        Returns:
            str: Generated report content
        """
        print("Generating comprehensive budget report...")
        
        # Generate text reports
        monthly_report = self.generate_monthly_summary(year, month, save_to_file)
        goals_report = self.generate_goals_summary(save_to_file)
        
        # Generate charts
        if save_to_file:
            print("Generating charts...")
            self.generate_spending_chart(year, month, save_to_file=True)
            self.generate_budget_status_chart(year, month, save_to_file=True)
            self.generate_goals_progress_chart(save_to_file=True)
            self.generate_income_vs_expenses_chart(year, month, save_to_file=True)
            self.generate_monthly_trend_chart(save_to_file=True)
        
        # Combine reports
        comprehensive_content = []
        comprehensive_content.append("COMPREHENSIVE BUDGET REPORT")
        comprehensive_content.append("=" * 50)
        comprehensive_content.append("")
        comprehensive_content.append(monthly_report)
        comprehensive_content.append("")
        comprehensive_content.append("=" * 50)
        comprehensive_content.append("")
        comprehensive_content.append(goals_report)
        
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.reports_dir}/comprehensive_report_{year}_{month:02d}_{timestamp}.txt"
            with open(filename, 'w') as f:
                f.write("\n".join(comprehensive_content))
            print(f"Comprehensive report saved to: {filename}")
        
        return "\n".join(comprehensive_content)


# TODO: Add multi-month comparison charts for spending trends
# TODO: Add category heatmaps in reports
# TODO: Add goal completion notifications (console or email)
# TODO: Fix bug: totals sometimes miscalculate if income added before budget setup
# TODO: Add export to CSV/XLSX option
# TODO: Add dark mode support for charts
# TODO: Implement unit tests for budget and goal modules
