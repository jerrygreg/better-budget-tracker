#!/usr/bin/env python3
"""
Budget Tracker CLI Application.

This is the main entry point for the budget tracker application.
It provides a command-line interface for managing budgets, expenses, income, and savings goals.
"""

import sys
import os
from typing import TypeVar, Callable
from datetime import datetime, date

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from budget import BudgetManager, IncomeEntry, ExpenseEntry, BudgetLimit
from goal_tracker import GoalTracker, SavingsGoal
from reports import ReportGenerator
from utils import (
    validate_amount, validate_date, validate_category, validate_description,
    parse_amount, format_currency, format_date, format_percentage,
    get_common_expense_categories, get_common_income_sources, get_common_goal_categories,
    get_current_date_string, get_month_start_date, get_month_end_date
)


class BudgetTrackerCLI:
    """Command-line interface for the budget tracker."""
    
    def __init__(self):
        """Initialize the CLI application."""
        self.console = Console()
        self.budget_manager = BudgetManager()
        self.goal_tracker = GoalTracker()
        self.report_generator = ReportGenerator(self.budget_manager, self.goal_tracker)
        self.running = True
    
    def display_welcome(self) -> None:
        """Display welcome message and main menu."""
        welcome_text = """
        💰 BUDGET PLANNER & FINANCIAL GOALS TRACKER 💰
        
        Track your income, expenses, budgets, and savings goals
        to achieve financial success!
        """
        
        self.console.print(Panel(welcome_text, title="Welcome", border_style="green"))
    
    def display_main_menu(self) -> None:
        """Display the main menu options."""
        menu_options = [
            "💰 Income Management",
            "💸 Expense Management", 
            "📊 Budget Management",
            "🎯 Savings Goals",
            "📈 Reports & Analytics",
            "🔍 Search & View Data",
            "❌ Exit"
        ]
        
        table = Table(title="Main Menu", show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        
        descriptions = [
            "Add and manage income entries",
            "Add and manage expense entries",
            "Set and view budget limits",
            "Create and track savings goals",
            "Generate reports and charts",
            "Search and view all data",
            "Exit the application"
        ]
        
        for i, (option, desc) in enumerate(zip(menu_options, descriptions), 1):
            table.add_row(f"{i}", f"{option} - {desc}")
        
        self.console.print(table)
    
    def get_user_choice(self) -> str:
        """Get user's menu choice."""
        while True:
            try:
                choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6", "7"])
                return choice
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Exiting...[/yellow]")
                sys.exit(0)

    TParseReturnType = TypeVar("TParseReturnType")

    def get_parsed_input(self, prompt: str,
                         parse: Callable[[str], TParseReturnType] = None,
                         default=None) -> TParseReturnType:
        """Get user input and parse with provided function"""
        while True:
            user_input = Prompt.ask(prompt, default=default)
            if parse is not None:
                try:
                    return parse(user_input)
                except ValueError as e:
                    self.console.print(f"[red]{e}[/red]")

    def get_validated_input(self, prompt: str, error_message: str,
                            validate: Callable[[str], bool] = None,
                            default=None) -> str:
        """Get user input and validate with provided function"""
        while True:
            user_input = Prompt.ask(prompt, default=default)
            if validate is not None:
                if not validate(user_input):
                    self.console.print(
                        f"[red]{error_message}[/red]")
                else:
                    return user_input

    def income_management_menu(self) -> None:
        """Handle income management operations."""
        while True:
            self.console.print("\n[bold blue]💰 Income Management[/bold blue]")
            self.console.print("1. Add Income Entry")
            self.console.print("2. View All Income")
            self.console.print("3. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])
            
            if choice == "1":
                self.add_income_entry()
            elif choice == "2":
                self.view_all_income()
            elif choice == "3":
                break
    
    def add_income_entry(self) -> None:
        """Add a new income entry."""
        self.console.print("\n[bold green]Add Income Entry[/bold green]")
        
        try:
            # Get income source
            common_sources = get_common_income_sources()
            self.console.print(f"Common sources: {', '.join(common_sources)}")
            source_input = self.get_validated_input("Income source",
                                                    "Invalid source name.",
                                                    validate=validate_category)

            # Get amount
            amount_input = self.get_parsed_input("Amount", parse=parse_amount)

            # Get date
            date_input = self.get_validated_input("Date (YYYY-MM-DD)",
                                                  "Invalid date format",
                                                  validate=validate_date,
                                                  default=get_current_date_string())

            # Get description
            description_input = self.get_validated_input(
                "Description (optional)",
                "Description too long",
                validate=validate_description,
                default="")

            # Create and add income entry
            income = IncomeEntry(
                date=date_input,
                source=source_input,
                amount=amount_input,
                description=description_input
            )
            
            income_id = self.budget_manager.add_income(income)
            self.console.print(f"[green]✅ Income entry added successfully with ID: {income_id}[/green]")
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error adding income: {e}[/red]")
    
    def view_all_income(self) -> None:
        """View all income entries."""
        income_entries = self.budget_manager.get_all_income()
        
        if not income_entries:
            self.console.print("[yellow]No income entries found.[/yellow]")
            return
        
        table = Table(title="All Income Entries", show_header=True, header_style="bold green")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Date", style="white")
        table.add_column("Source", style="green")
        table.add_column("Amount", style="green", justify="right")
        table.add_column("Description", style="white")
        
        for income in income_entries:
            table.add_row(
                str(income.id),
                format_date(income.date, output_format='%Y-%m-%d'),
                income.source,
                format_currency(income.amount),
                income.description[:30] + "..." if len(income.description) > 30 else income.description
            )
        
        self.console.print(table)
        
        # Show summary
        total_income = sum(income.amount for income in income_entries)
        self.console.print(f"\n[bold green]Total Income: {format_currency(total_income)}[/bold green]")
    
    def expense_management_menu(self) -> None:
        """Handle expense management operations."""
        while True:
            self.console.print("\n[bold red]💸 Expense Management[/bold red]")
            self.console.print("1. Add Expense Entry")
            self.console.print("2. View All Expenses")
            self.console.print("3. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])
            
            if choice == "1":
                self.add_expense_entry()
            elif choice == "2":
                self.view_all_expenses()
            elif choice == "3":
                break
    
    def add_expense_entry(self) -> None:
        """Add a new expense entry."""
        self.console.print("\n[bold red]Add Expense Entry[/bold red]")
        
        try:
            # Get category
            common_categories = get_common_expense_categories()
            self.console.print(
                f"Common categories: {', '.join(common_categories)}")
            category_input = self.get_validated_input("Expense category",
                                                      "Invalid category name.",
                                                      validate=validate_category)

            # Get amount
            amount_input = self.get_parsed_input("Amount", parse=parse_amount)

            # Get date
            date_input = self.get_validated_input("Date (YYYY-MM-DD)",
                                                  "Invalid date format",
                                                  validate=validate_date,
                                                  default=get_current_date_string())

            # Get description
            description_input = self.get_validated_input(
                "Description (optional)",
                "Description too long",
                validate=validate_description,
                default="")

            # Create and add expense entry
            expense = ExpenseEntry(
                date=date_input,
                category=category_input,
                amount=amount_input,
                description=description_input
            )

            expense_id = self.budget_manager.add_expense(expense)
            self.console.print(f"[green]✅ Expense entry added successfully with ID: {expense_id}[/green]")
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error adding expense: {e}[/red]")
    
    def view_all_expenses(self) -> None:
        """View all expense entries."""
        expense_entries = self.budget_manager.get_all_expenses()
        
        if not expense_entries:
            self.console.print("[yellow]No expense entries found.[/yellow]")
            return
        
        table = Table(title="All Expense Entries", show_header=True, header_style="bold red")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Date", style="white")
        table.add_column("Category", style="red")
        table.add_column("Amount", style="red", justify="right")
        table.add_column("Description", style="white")
        
        for expense in expense_entries:
            table.add_row(
                str(expense.id),
                format_date(expense.date, output_format='%Y-%m-%d'),
                expense.category,
                format_currency(expense.amount),
                expense.description[:30] + "..." if len(expense.description) > 30 else expense.description
            )
        
        self.console.print(table)
        
        # Show summary
        total_expenses = sum(expense.amount for expense in expense_entries)
        self.console.print(f"\n[bold red]Total Expenses: {format_currency(total_expenses)}[/bold red]")
    
    def budget_management_menu(self) -> None:
        """Handle budget management operations."""
        while True:
            self.console.print("\n[bold blue]📊 Budget Management[/bold blue]")
            self.console.print("1. Set Budget Limit")
            self.console.print("2. View Budget Status")
            self.console.print("3. View All Budget Limits")
            self.console.print("4. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])
            
            if choice == "1":
                self.set_budget_limit()
            elif choice == "2":
                self.view_budget_status()
            elif choice == "3":
                self.view_all_budget_limits()
            elif choice == "4":
                break
    
    def set_budget_limit(self) -> None:
        """Set a budget limit for a category."""
        self.console.print("\n[bold blue]Set Budget Limit[/bold blue]")
        
        try:
            # Get category
            common_categories = get_common_expense_categories()
            self.console.print(f"Common categories: {', '.join(common_categories)}")
            category = Prompt.ask("Category")
            
            if not validate_category(category):
                self.console.print("[red]Invalid category name.[/red]")
                return
            
            # Get monthly limit
            limit_input = Prompt.ask("Monthly budget limit")
            try:
                monthly_limit = parse_amount(limit_input)
            except ValueError as e:
                self.console.print(f"[red]Invalid amount: {e}[/red]")
                return
            
            # Get description
            description = Prompt.ask("Description (optional)", default="")
            if not validate_description(description):
                self.console.print("[red]Description too long.[/red]")
                return
            
            # Create and set budget limit
            budget_limit = BudgetLimit(
                category=category,
                monthly_limit=monthly_limit,
                description=description
            )
            
            budget_id = self.budget_manager.set_budget_limit(budget_limit)
            self.console.print(f"[green]✅ Budget limit set successfully with ID: {budget_id}[/green]")
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error setting budget limit: {e}[/red]")
    
    def view_budget_status(self) -> None:
        """View current budget status."""
        current_date = date.today()
        budget_status = self.budget_manager.get_budget_status(current_date.year, current_date.month)
        
        if not budget_status:
            self.console.print("[yellow]No budget limits set.[/yellow]")
            return
        
        table = Table(title=f"Budget Status - {format_date(f'{current_date.year}-{current_date.month:02d}-01', output_format='%B %Y')}", 
                     show_header=True, header_style="bold blue")
        table.add_column("Category", style="cyan")
        table.add_column("Limit", style="white", justify="right")
        table.add_column("Spent", style="red", justify="right")
        table.add_column("Remaining", style="green", justify="right")
        table.add_column("Status", style="white")
        
        for category, status in budget_status.items():
            status_icon = "🔴" if status['is_over_budget'] else "🟢"
            remaining = format_currency(status['remaining']) if status['remaining'] > 0 else "₹0.00"
            
            table.add_row(
                category,
                format_currency(status['limit']),
                format_currency(status['spent']),
                remaining,
                f"{status_icon} {status['percentage_used']:.1f}%"
            )
        
        self.console.print(table)
        
        # Show overspending alerts
        overspending_alerts = self.budget_manager.get_overspending_alerts(current_date.year, current_date.month)
        if overspending_alerts:
            self.console.print("\n[bold red]⚠️  OVERSPENDING ALERTS[/bold red]")
            for alert in overspending_alerts:
                self.console.print(f"[red]• {alert['category']}: Over by {format_currency(alert['overspent'])} "
                                 f"({alert['percentage_over']:.1f}% over limit)[/red]")
    
    def view_all_budget_limits(self) -> None:
        """View all budget limits."""
        budget_limits = self.budget_manager.get_all_budget_limits()
        
        if not budget_limits:
            self.console.print("[yellow]No budget limits set.[/yellow]")
            return
        
        table = Table(title="All Budget Limits", show_header=True, header_style="bold blue")
        table.add_column("Category", style="cyan")
        table.add_column("Monthly Limit", style="white", justify="right")
        table.add_column("Description", style="white")
        
        for budget_limit in budget_limits:
            table.add_row(
                budget_limit.category,
                format_currency(budget_limit.monthly_limit),
                budget_limit.description
            )
        
        self.console.print(table)
    
    def savings_goals_menu(self) -> None:
        """Handle savings goals operations."""
        while True:
            self.console.print("\n[bold yellow]🎯 Savings Goals[/bold yellow]")
            self.console.print("1. Create New Goal")
            self.console.print("2. View All Goals")
            self.console.print("3. Add Progress to Goal")
            self.console.print("4. View Goals Summary")
            self.console.print("5. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self.create_savings_goal()
            elif choice == "2":
                self.view_all_goals()
            elif choice == "3":
                self.add_goal_progress()
            elif choice == "4":
                self.view_goals_summary()
            elif choice == "5":
                break
    
    def create_savings_goal(self) -> None:
        """Create a new savings goal."""
        self.console.print("\n[bold yellow]Create Savings Goal[/bold yellow]")
        
        try:
            # Get goal name
            name = Prompt.ask("Goal name")
            if not name.strip():
                self.console.print("[red]Goal name cannot be empty.[/red]")
                return
            
            # Get target amount
            target_input = Prompt.ask("Target amount")
            try:
                target_amount = parse_amount(target_input)
            except ValueError as e:
                self.console.print(f"[red]Invalid amount: {e}[/red]")
                return
            
            # Get target date
            target_date = Prompt.ask("Target date (YYYY-MM-DD)")
            if not validate_date(target_date):
                self.console.print("[red]Invalid date format.[/red]")
                return
            
            # Get category
            common_categories = get_common_goal_categories()
            self.console.print(f"Common categories: {', '.join(common_categories)}")
            category = Prompt.ask("Category")
            
            if not validate_category(category):
                self.console.print("[red]Invalid category name.[/red]")
                return
            
            # Get description
            description = Prompt.ask("Description (optional)", default="")
            if not validate_description(description):
                self.console.print("[red]Description too long.[/red]")
                return
            
            # Create and add goal
            goal = SavingsGoal(
                name=name,
                target_amount=target_amount,
                current_amount=0.0,
                target_date=target_date,
                category=category,
                description=description,
                is_completed=False,
                created_date=get_current_date_string()
            )
            
            goal_id = self.goal_tracker.add_goal(goal)
            self.console.print(f"[green]✅ Savings goal created successfully with ID: {goal_id}[/green]")
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error creating goal: {e}[/red]")
    
    def view_all_goals(self) -> None:
        """View all savings goals."""
        goals = self.goal_tracker.get_all_goals()
        
        if not goals:
            self.console.print("[yellow]No savings goals found.[/yellow]")
            return
        
        table = Table(title="All Savings Goals", show_header=True, header_style="bold yellow")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="white")
        table.add_column("Category", style="yellow")
        table.add_column("Progress", style="green", justify="right")
        table.add_column("Target Date", style="white")
        table.add_column("Status", style="white")
        
        for goal in goals:
            status_icon = "✅" if goal.is_completed else "🔴" if goal.is_overdue else "🟡"
            progress_text = f"{format_currency(goal.current_amount)} / {format_currency(goal.target_amount)}"
            
            table.add_row(
                str(goal.id),
                goal.name,
                goal.category,
                progress_text,
                format_date(goal.target_date, output_format='%Y-%m-%d'),
                f"{status_icon} {goal.progress_percentage:.1f}%"
            )
        
        self.console.print(table)
    
    def add_goal_progress(self) -> None:
        """Add progress to a savings goal."""
        self.console.print("\n[bold yellow]Add Progress to Goal[/bold yellow]")
        
        # First show all goals
        goals = self.goal_tracker.get_active_goals()
        if not goals:
            self.console.print("[yellow]No active goals found.[/yellow]")
            return
        
        self.view_all_goals()
        
        try:
            goal_id = int(Prompt.ask("Enter goal ID"))
            goal = self.goal_tracker.get_goal_by_id(goal_id)
            
            if not goal:
                self.console.print("[red]Goal not found.[/red]")
                return
            
            amount_input = Prompt.ask("Amount to add")
            try:
                amount = parse_amount(amount_input)
            except ValueError as e:
                self.console.print(f"[red]Invalid amount: {e}[/red]")
                return
            
            success = self.goal_tracker.add_progress(goal_id, amount)
            if success:
                self.console.print(f"[green]✅ Progress added successfully![/green]")
                if goal.current_amount >= goal.target_amount:
                    self.console.print(f"[bold green]🎉 Goal '{goal.name}' completed![/bold green]")
            else:
                self.console.print("[red]❌ Failed to add progress.[/red]")
                
        except ValueError:
            self.console.print("[red]Invalid goal ID.[/red]")
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            self.console.print(f"[red]❌ Error adding progress: {e}[/red]")
    
    def view_goals_summary(self) -> None:
        """View goals summary."""
        summary = self.goal_tracker.get_goals_summary()
        
        summary_text = f"""
        Total Goals: {summary['total_goals']}
        Active Goals: {summary['active_goals']}
        Completed Goals: {summary['completed_goals']}
        Overdue Goals: {summary['overdue_goals']}
        
        Total Target Amount: {format_currency(summary['total_target_amount'])}
        Total Current Amount: {format_currency(summary['total_current_amount'])}
        Total Remaining: {format_currency(summary['total_remaining'])}
        Overall Progress: {summary['overall_progress']:.1f}%
        """
        
        self.console.print(Panel(summary_text, title="Goals Summary", border_style="yellow"))
    
    def reports_menu(self) -> None:
        """Handle reports and analytics operations."""
        while True:
            self.console.print("\n[bold magenta]📈 Reports & Analytics[/bold magenta]")
            self.console.print("1. Monthly Summary Report")
            self.console.print("2. Goals Summary Report")
            self.console.print("3. Generate Charts")
            self.console.print("4. Comprehensive Report")
            self.console.print("5. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5"])
            
            if choice == "1":
                self.generate_monthly_report()
            elif choice == "2":
                self.generate_goals_report()
            elif choice == "3":
                self.generate_charts()
            elif choice == "4":
                self.generate_comprehensive_report()
            elif choice == "5":
                break
    
    def generate_monthly_report(self) -> None:
        """Generate monthly summary report."""
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating monthly report...", total=None)
            self.report_generator.generate_monthly_summary(year, month)
        
        self.console.print("[green]✅ Monthly summary report generated![/green]")
    
    def generate_goals_report(self) -> None:
        """Generate goals summary report."""
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating goals report...", total=None)
            self.report_generator.generate_goals_summary()
        
        self.console.print("[green]✅ Goals summary report generated![/green]")
    
    def generate_charts(self) -> None:
        """Generate various charts."""
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating charts...", total=None)
            
            self.report_generator.generate_spending_chart(year, month)
            self.report_generator.generate_budget_status_chart(year, month)
            self.report_generator.generate_goals_progress_chart()
            self.report_generator.generate_income_vs_expenses_chart(year, month)
            self.report_generator.generate_monthly_trend_chart()
        
        self.console.print("[green]✅ All charts generated![/green]")
    
    def generate_comprehensive_report(self) -> None:
        """Generate comprehensive report."""
        current_date = date.today()
        year = current_date.year
        month = current_date.month
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating comprehensive report...", total=None)
            self.report_generator.generate_comprehensive_report(year, month)
        
        self.console.print("[green]✅ Comprehensive report generated![/green]")
    
    def search_menu(self) -> None:
        """Handle search and view data operations."""
        while True:
            self.console.print("\n[bold cyan]🔍 Search & View Data[/bold cyan]")
            self.console.print("1. Search Entries")
            self.console.print("2. View Monthly Summary")
            self.console.print("3. Back to Main Menu")
            
            choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])
            
            if choice == "1":
                self.search_entries()
            elif choice == "2":
                self.view_monthly_summary()
            elif choice == "3":
                break
    
    def search_entries(self) -> None:
        """Search income and expense entries."""
        query = Prompt.ask("Enter search term")
        
        if not query.strip():
            self.console.print("[yellow]Search term cannot be empty.[/yellow]")
            return
        
        matching_income, matching_expenses = self.budget_manager.search_entries(query)
        
        if not matching_income and not matching_expenses:
            self.console.print(f"[yellow]No entries found matching '{query}'.[/yellow]")
            return
        
        if matching_income:
            self.console.print(f"\n[bold green]Income Entries ({len(matching_income)})[/bold green]")
            table = Table(show_header=True, header_style="bold green")
            table.add_column("Date", style="white")
            table.add_column("Source", style="green")
            table.add_column("Amount", style="green", justify="right")
            table.add_column("Description", style="white")
            
            for income in matching_income:
                table.add_row(
                    format_date(income.date, output_format='%Y-%m-%d'),
                    income.source,
                    format_currency(income.amount),
                    income.description
                )
            
            self.console.print(table)
        
        if matching_expenses:
            self.console.print(f"\n[bold red]Expense Entries ({len(matching_expenses)})[/bold red]")
            table = Table(show_header=True, header_style="bold red")
            table.add_column("Date", style="white")
            table.add_column("Category", style="red")
            table.add_column("Amount", style="red", justify="right")
            table.add_column("Description", style="white")
            
            for expense in matching_expenses:
                table.add_row(
                    format_date(expense.date, output_format='%Y-%m-%d'),
                    expense.category,
                    format_currency(expense.amount),
                    expense.description
                )
            
            self.console.print(table)
    
    def view_monthly_summary(self) -> None:
        """View monthly financial summary."""
        current_date = date.today()
        monthly_summary = self.budget_manager.get_monthly_summary(current_date.year, current_date.month)
        
        summary_text = f"""
        Month: {format_date(f'{current_date.year}-{current_date.month:02d}-01', output_format='%B %Y')}
        
        Total Income: {format_currency(monthly_summary['total_income'])}
        Total Expenses: {format_currency(monthly_summary['total_expenses'])}
        Net Income: {format_currency(monthly_summary['net_income'])}
        Savings Rate: {monthly_summary['savings_rate']:.1f}%
        """
        
        self.console.print(Panel(summary_text, title="Monthly Summary", border_style="blue"))
    
    def run(self) -> None:
        """Run the main application loop."""
        self.display_welcome()
        
        while self.running:
            try:
                self.display_main_menu()
                choice = self.get_user_choice()
                
                if choice == "1":
                    self.income_management_menu()
                elif choice == "2":
                    self.expense_management_menu()
                elif choice == "3":
                    self.budget_management_menu()
                elif choice == "4":
                    self.savings_goals_menu()
                elif choice == "5":
                    self.reports_menu()
                elif choice == "6":
                    self.search_menu()
                elif choice == "7":
                    self.console.print("\n[bold green]Thank you for using Budget Tracker![/bold green]")
                    self.running = False
                
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Exiting...[/yellow]")
                self.running = False
            except Exception as e:
                self.console.print(f"\n[red]❌ Unexpected error: {e}[/red]")


def main():
    """Main entry point for the application."""
    try:
        app = BudgetTrackerCLI()
        app.run()
    except Exception as e:
        console = Console()
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()


# TODO: Add multi-month comparison charts for spending trends
# TODO: Add category heatmaps in reports
# TODO: Add goal completion notifications (console or email)
# TODO: Fix bug: totals sometimes miscalculate if income added before budget setup
# TODO: Add export to CSV/XLSX option
# TODO: Add dark mode support for charts
# TODO: Implement unit tests for budget and goal modules
