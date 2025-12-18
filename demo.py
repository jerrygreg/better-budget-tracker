#!/usr/bin/env python3
"""
Demo script for Budget Tracker.

This script demonstrates the functionality of the budget tracker
by adding some sample data and generating reports.
"""

from src.better_budget_tracker.budget import BudgetManager, IncomeEntry, ExpenseEntry, BudgetLimit
from src.better_budget_tracker.goal_tracker import GoalTracker, SavingsGoal
from reports import ReportGenerator
from datetime import date


def create_sample_data():
    """Create sample budget data for demonstration."""
    budget_manager = BudgetManager()
    goal_tracker = GoalTracker()
    
    # Sample income entries
    sample_income = [
        IncomeEntry(
            date="2024-01-01",
            source="Salary",
            amount=50000.0,
            description="Monthly salary"
        ),
        IncomeEntry(
            date="2024-01-15",
            source="Freelance",
            amount=15000.0,
            description="Web development project"
        ),
        IncomeEntry(
            date="2024-01-20",
            source="Investment",
            amount=5000.0,
            description="Dividend income"
        )
    ]
    
    # Sample expense entries
    sample_expenses = [
        ExpenseEntry(
            date="2024-01-02",
            category="Housing",
            amount=15000.0,
            description="Monthly rent"
        ),
        ExpenseEntry(
            date="2024-01-03",
            category="Food & Dining",
            amount=3000.0,
            description="Grocery shopping"
        ),
        ExpenseEntry(
            date="2024-01-05",
            category="Transportation",
            amount=2000.0,
            description="Fuel and public transport"
        ),
        ExpenseEntry(
            date="2024-01-10",
            category="Entertainment",
            amount=1500.0,
            description="Movie tickets and dinner"
        ),
        ExpenseEntry(
            date="2024-01-12",
            category="Utilities",
            amount=2500.0,
            description="Electricity and internet bills"
        ),
        ExpenseEntry(
            date="2024-01-15",
            category="Food & Dining",
            amount=2000.0,
            description="Restaurant meals"
        ),
        ExpenseEntry(
            date="2024-01-18",
            category="Shopping",
            amount=4000.0,
            description="Clothing and accessories"
        ),
        ExpenseEntry(
            date="2024-01-22",
            category="Healthcare",
            amount=1200.0,
            description="Doctor visit and medicines"
        )
    ]
    
    # Sample budget limits
    sample_budgets = [
        BudgetLimit(
            category="Housing",
            monthly_limit=15000.0,
            description="Monthly rent budget"
        ),
        BudgetLimit(
            category="Food & Dining",
            monthly_limit=5000.0,
            description="Food and dining budget"
        ),
        BudgetLimit(
            category="Transportation",
            monthly_limit=3000.0,
            description="Transportation budget"
        ),
        BudgetLimit(
            category="Entertainment",
            monthly_limit=2000.0,
            description="Entertainment budget"
        ),
        BudgetLimit(
            category="Utilities",
            monthly_limit=3000.0,
            description="Utilities budget"
        ),
        BudgetLimit(
            category="Shopping",
            monthly_limit=5000.0,
            description="Shopping budget"
        ),
        BudgetLimit(
            category="Healthcare",
            monthly_limit=2000.0,
            description="Healthcare budget"
        )
    ]
    
    # Sample savings goals
    sample_goals = [
        SavingsGoal(
            name="Emergency Fund",
            target_amount=100000.0,
            current_amount=25000.0,
            target_date="2024-12-31",
            category="Emergency Fund",
            description="6 months of expenses",
            is_completed=False,
            created_date="2024-01-01"
        ),
        SavingsGoal(
            name="Vacation to Europe",
            target_amount=200000.0,
            current_amount=75000.0,
            target_date="2024-06-30",
            category="Vacation",
            description="2-week Europe trip",
            is_completed=False,
            created_date="2024-01-01"
        ),
        SavingsGoal(
            name="New Laptop",
            target_amount=80000.0,
            current_amount=80000.0,
            target_date="2024-03-15",
            category="Gadgets",
            description="MacBook Pro for work",
            is_completed=True,
            created_date="2024-01-01"
        ),
        SavingsGoal(
            name="Home Down Payment",
            target_amount=500000.0,
            current_amount=150000.0,
            target_date="2025-12-31",
            category="Home Purchase",
            description="20% down payment for house",
            is_completed=False,
            created_date="2024-01-01"
        )
    ]
    
    print("Adding sample data...")
    
    # Add income entries
    for income in sample_income:
        try:
            income_id = budget_manager.add_income(income)
            print(f"✅ Added income: {income.source} - ${income.amount:,.2f} (ID: {income_id})")
        except Exception as e:
            print(f"❌ Failed to add income {income.source}: {e}")
    
    # Add expense entries
    for expense in sample_expenses:
        try:
            expense_id = budget_manager.add_expense(expense)
            print(f"✅ Added expense: {expense.category} - ${expense.amount:,.2f} (ID: {expense_id})")
        except Exception as e:
            print(f"❌ Failed to add expense {expense.category}: {e}")
    
    # Add budget limits
    for budget in sample_budgets:
        try:
            budget_id = budget_manager.set_budget_limit(budget)
            print(f"✅ Set budget limit: {budget.category} - ${budget.monthly_limit:,.2f} (ID: {budget_id})")
        except Exception as e:
            print(f"❌ Failed to set budget limit {budget.category}: {e}")
    
    # Add savings goals
    for goal in sample_goals:
        try:
            goal_id = goal_tracker.add_goal(goal)
            print(f"✅ Added goal: {goal.name} - ${goal.target_amount:,.2f} (ID: {goal_id})")
        except Exception as e:
            print(f"❌ Failed to add goal {goal.name}: {e}")
    
    return budget_manager, goal_tracker


def demonstrate_features(budget_manager, goal_tracker):
    """Demonstrate various features of the budget tracker."""
    print("\n" + "="*60)
    print("BUDGET TRACKER DEMONSTRATION")
    print("="*60)
    
    # Monthly summary
    current_date = date.today()
    monthly_summary = budget_manager.get_monthly_summary(current_date.year, current_date.month)
    
    print(f"\n1. MONTHLY FINANCIAL SUMMARY:")
    print("-" * 35)
    print(f"Total Income: ${monthly_summary['total_income']:,.2f}")
    print(f"Total Expenses: ${monthly_summary['total_expenses']:,.2f}")
    print(f"Net Income: ${monthly_summary['net_income']:,.2f}")
    print(f"Savings Rate: {monthly_summary['savings_rate']:.1f}%")
    
    # Budget status
    print(f"\n2. BUDGET STATUS:")
    print("-" * 20)
    budget_status = budget_manager.get_budget_status(current_date.year, current_date.month)
    for category, status in budget_status.items():
        status_icon = "🔴" if status['is_over_budget'] else "🟢"
        print(f"{status_icon} {category}: ${status['spent']:,.2f} / ${status['limit']:,.2f} "
              f"({status['percentage_used']:.1f}%)")
    
    # Overspending alerts
    overspending_alerts = budget_manager.get_overspending_alerts(current_date.year, current_date.month)
    if overspending_alerts:
        print(f"\n3. OVERSPENDING ALERTS:")
        print("-" * 25)
        for alert in overspending_alerts:
            print(f"⚠️  {alert['category']}: Over by ${alert['overspent']:,.2f} "
                  f"({alert['percentage_over']:.1f}% over limit)")
    
    # Category breakdown
    print(f"\n4. EXPENSE BREAKDOWN BY CATEGORY:")
    print("-" * 40)
    category_summary = budget_manager.get_category_summary(current_date.year, current_date.month)
    total_expenses = sum(category_summary.values())
    for category, amount in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
        print(f"{category}: ${amount:,.2f} ({percentage:.1f}%)")
    
    # Goals summary
    print(f"\n5. SAVINGS GOALS SUMMARY:")
    print("-" * 30)
    goals_summary = goal_tracker.get_goals_summary()
    print(f"Total Goals: {goals_summary['total_goals']}")
    print(f"Active Goals: {goals_summary['active_goals']}")
    print(f"Completed Goals: {goals_summary['completed_goals']}")
    print(f"Overdue Goals: {goals_summary['overdue_goals']}")
    print(f"Total Target Amount: ${goals_summary['total_target_amount']:,.2f}")
    print(f"Total Current Amount: ${goals_summary['total_current_amount']:,.2f}")
    print(f"Total Remaining: ${goals_summary['total_remaining']:,.2f}")
    print(f"Overall Progress: {goals_summary['overall_progress']:.1f}%")
    
    # Active goals details
    active_goals = goal_tracker.get_active_goals()
    if active_goals:
        print(f"\n6. ACTIVE GOALS DETAILS:")
        print("-" * 30)
        for goal in active_goals:
            status_icon = "🔴" if goal.is_overdue else "🟡"
            print(f"{status_icon} {goal.name} ({goal.category})")
            print(f"   Progress: ${goal.current_amount:,.2f} / ${goal.target_amount:,.2f} "
                  f"({goal.progress_percentage:.1f}%)")
            print(f"   Target Date: {goal.target_date} ({goal.days_remaining} days remaining)")
    
    # Completed goals
    completed_goals = goal_tracker.get_completed_goals()
    if completed_goals:
        print(f"\n7. COMPLETED GOALS:")
        print("-" * 20)
        for goal in completed_goals:
            print(f"✅ {goal.name} ({goal.category}) - ${goal.target_amount:,.2f}")


def generate_sample_reports(budget_manager, goal_tracker):
    """Generate sample reports."""
    print(f"\n8. GENERATING REPORTS:")
    print("-" * 25)
    
    report_generator = ReportGenerator(budget_manager, goal_tracker)
    current_date = date.today()
    
    try:
        print("Generating monthly summary report...")
        report_generator.generate_monthly_summary(current_date.year, current_date.month)
        print("✅ Monthly summary report generated")
        
        print("Generating goals summary report...")
        report_generator.generate_goals_summary()
        print("✅ Goals summary report generated")
        
        print("Generating spending chart...")
        report_generator.generate_spending_chart(current_date.year, current_date.month)
        print("✅ Spending chart generated")
        
        print("Generating budget status chart...")
        report_generator.generate_budget_status_chart(current_date.year, current_date.month)
        print("✅ Budget status chart generated")
        
        print("Generating goals progress chart...")
        report_generator.generate_goals_progress_chart()
        print("✅ Goals progress chart generated")
        
        print("Generating income vs expenses chart...")
        report_generator.generate_income_vs_expenses_chart(current_date.year, current_date.month)
        print("✅ Income vs expenses chart generated")
        
        print("Generating monthly trend chart...")
        report_generator.generate_monthly_trend_chart()
        print("✅ Monthly trend chart generated")
        
        print("\nAll reports saved to the 'reports/' directory!")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")


def main():
    """Main demonstration function."""
    print("Budget Tracker Demo")
    print("This demo will create sample data and demonstrate features.")
    
    try:
        # Create sample data
        budget_manager, goal_tracker = create_sample_data()
        
        # Demonstrate features
        demonstrate_features(budget_manager, goal_tracker)
        
        # Generate reports
        generate_sample_reports(budget_manager, goal_tracker)
        
        print(f"\n" + "="*60)
        print("DEMO COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("You can now:")
        print("• Run 'python main.py' for the CLI interface")
        print("• Check the 'reports/' directory for generated files")
        print("• Check the 'data/' directory for the database")
        print("• Use the search functionality to find specific entries")
        print("• Generate custom reports for different months")
        print("• Track your own financial data")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")


if __name__ == "__main__":
    main()
