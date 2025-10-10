"""
Utility functions for the budget tracker.

This module contains helper functions for validation, date parsing,
formatting, and other common operations used throughout the application.
"""

import re
from datetime import datetime, date, timedelta
from typing import Optional, List, Tuple, Union


def validate_amount(amount: Union[str, float, int]) -> bool:
    """
    Validate if an amount is a valid positive number.
    
    Args:
        amount: Amount to validate
        
    Returns:
        bool: True if amount is valid, False otherwise
    """
    try:
        if isinstance(amount, str):
            # Remove currency symbols and spaces
            cleaned = re.sub(r'[₹$€£¥\s,]', '', amount.strip())
            value = float(cleaned)
        else:
            value = float(amount)
        
        return value >= 0
    except (ValueError, TypeError):
        return False


def parse_amount(amount_input: str) -> float:
    """
    Parse an amount string and return a float value.
    
    Args:
        amount_input: Amount string (e.g., "1000", "₹1,000", "$100.50")
        
    Returns:
        float: Parsed amount value
        
    Raises:
        ValueError: If amount string cannot be parsed
    """
    if not amount_input:
        raise ValueError("Amount cannot be empty")
    
    # Remove currency symbols, spaces, and commas
    cleaned = re.sub(r'[₹$€£¥\s,]', '', amount_input.strip())
    
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError(f"Invalid amount format: {amount_input}")


def format_currency(amount: float, currency_symbol: str = "₹") -> str:
    """
    Format a float amount as currency string.
    
    Args:
        amount: Amount to format
        currency_symbol: Currency symbol to use
        
    Returns:
        str: Formatted currency string
    """
    return f"{currency_symbol}{amount:,.2f}"


def validate_date(date_string: str) -> bool:
    """
    Validate if a date string is in the correct format (YYYY-MM-DD).
    
    Args:
        date_string: Date string to validate
        
    Returns:
        bool: True if date is valid, False otherwise
    """
    if not date_string:
        return False
    
    # Check format with regex
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(date_pattern, date_string):
        return False
    
    try:
        # Try to parse the date
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def format_date(date_string: str, input_format: str = '%Y-%m-%d', output_format: str = '%B %d, %Y') -> str:
    """
    Format a date string from one format to another.
    
    Args:
        date_string: Date string to format
        input_format: Format of the input date string
        output_format: Desired output format
        
    Returns:
        str: Formatted date string
        
    Raises:
        ValueError: If date string is invalid
    """
    try:
        date_obj = datetime.strptime(date_string, input_format)
        return date_obj.strftime(output_format)
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")


def get_current_date_string() -> str:
    """
    Get current date as a string in YYYY-MM-DD format.
    
    Returns:
        str: Current date string
    """
    return date.today().strftime('%Y-%m-%d')


def get_month_start_date(target_date: str) -> str:
    """
    Get the start date of the month for a given date.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        str: Start date of the month in YYYY-MM-DD format
    """
    if not validate_date(target_date):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
    month_start = date_obj.replace(day=1)
    
    return month_start.strftime('%Y-%m-%d')


def get_month_end_date(target_date: str) -> str:
    """
    Get the end date of the month for a given date.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        str: End date of the month in YYYY-MM-DD format
    """
    if not validate_date(target_date):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
    
    # Get first day of next month, then subtract one day
    if date_obj.month == 12:
        next_month = date_obj.replace(year=date_obj.year + 1, month=1, day=1)
    else:
        next_month = date_obj.replace(month=date_obj.month + 1, day=1)
    
    month_end = next_month - timedelta(days=1)
    
    return month_end.strftime('%Y-%m-%d')


def get_date_range_days(start_date: str, end_date: str) -> int:
    """
    Calculate the number of days between two dates.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        int: Number of days between dates
    """
    if not validate_date(start_date) or not validate_date(end_date):
        raise ValueError("Invalid date format")
    
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    return (end - start).days


def is_date_in_range(check_date: str, start_date: str, end_date: str) -> bool:
    """
    Check if a date falls within a given range.
    
    Args:
        check_date: Date to check in YYYY-MM-DD format
        start_date: Start of range in YYYY-MM-DD format
        end_date: End of range in YYYY-MM-DD format
        
    Returns:
        bool: True if date is in range, False otherwise
    """
    if not all(validate_date(d) for d in [check_date, start_date, end_date]):
        raise ValueError("Invalid date format")
    
    check = datetime.strptime(check_date, '%Y-%m-%d').date()
    start = datetime.strptime(start_date, '%Y-%m-%d').date()
    end = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    return start <= check <= end


def get_common_expense_categories() -> List[str]:
    """
    Get a list of common expense categories.
    
    Returns:
        List[str]: List of common categories
    """
    return [
        "Food & Dining",
        "Transportation",
        "Housing",
        "Utilities",
        "Entertainment",
        "Shopping",
        "Healthcare",
        "Education",
        "Travel",
        "Insurance",
        "Savings",
        "Other"
    ]


def get_common_income_sources() -> List[str]:
    """
    Get a list of common income sources.
    
    Returns:
        List[str]: List of common income sources
    """
    return [
        "Salary",
        "Freelance",
        "Investment",
        "Business",
        "Rental Income",
        "Bonus",
        "Gift",
        "Refund",
        "Other"
    ]


def get_common_goal_categories() -> List[str]:
    """
    Get a list of common savings goal categories.
    
    Returns:
        List[str]: List of common goal categories
    """
    return [
        "Emergency Fund",
        "Vacation",
        "Education",
        "Home Purchase",
        "Car Purchase",
        "Wedding",
        "Retirement",
        "Investment",
        "Gadgets",
        "Other"
    ]


def validate_category(category: str) -> bool:
    """
    Validate category name.
    
    Args:
        category: Category to validate
        
    Returns:
        bool: True if category is valid, False otherwise
    """
    if not category or not category.strip():
        return False
    
    # Check for reasonable length
    if len(category.strip()) < 1 or len(category.strip()) > 50:
        return False
    
    return True


def validate_description(description: str) -> bool:
    """
    Validate description text.
    
    Args:
        description: Description to validate
        
    Returns:
        bool: True if description is valid, False otherwise
    """
    if not description:
        return True  # Description is optional
    
    # Check for reasonable length
    if len(description.strip()) > 500:
        return False
    
    return True


def truncate_string(text: str, max_length: int = 30) -> str:
    """
    Truncate a string to a maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length of the result
        
    Returns:
        str: Truncated string with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def format_percentage(value: float, total: float) -> str:
    """
    Format a percentage value.
    
    Args:
        value: Current value
        total: Total value
        
    Returns:
        str: Formatted percentage string
    """
    if total == 0:
        return "0.0%"
    
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"


def format_progress_bar(current: float, total: float, width: int = 20) -> str:
    """
    Create a text-based progress bar.
    
    Args:
        current: Current value
        total: Total value
        width: Width of the progress bar
        
    Returns:
        str: Text-based progress bar
    """
    if total == 0:
        return "[" + " " * width + "] 0.0%"
    
    percentage = current / total
    filled_width = int(percentage * width)
    bar = "█" * filled_width + "░" * (width - filled_width)
    
    return f"[{bar}] {percentage * 100:.1f}%"


def calculate_monthly_average(values: List[float], months: int) -> float:
    """
    Calculate monthly average from a list of values.
    
    Args:
        values: List of values
        months: Number of months
        
    Returns:
        float: Monthly average
    """
    if not values or months == 0:
        return 0.0
    
    return sum(values) / months


def get_financial_year_start(target_date: str) -> str:
    """
    Get the start of the financial year for a given date.
    Assumes financial year starts in April.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        str: Financial year start date in YYYY-MM-DD format
    """
    if not validate_date(target_date):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
    
    # If month is April or later, financial year started this year
    if date_obj.month >= 4:
        fy_start = date_obj.replace(month=4, day=1)
    else:
        # Otherwise, financial year started last year
        fy_start = date_obj.replace(year=date_obj.year - 1, month=4, day=1)
    
    return fy_start.strftime('%Y-%m-%d')


def get_quarter_start(target_date: str) -> str:
    """
    Get the start of the quarter for a given date.
    
    Args:
        target_date: Date in YYYY-MM-DD format
        
    Returns:
        str: Quarter start date in YYYY-MM-DD format
    """
    if not validate_date(target_date):
        raise ValueError("Invalid date format")
    
    date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
    
    # Determine quarter start month
    if date_obj.month in [1, 2, 3]:
        quarter_start_month = 1
    elif date_obj.month in [4, 5, 6]:
        quarter_start_month = 4
    elif date_obj.month in [7, 8, 9]:
        quarter_start_month = 7
    else:
        quarter_start_month = 10
    
    quarter_start = date_obj.replace(month=quarter_start_month, day=1)
    
    return quarter_start.strftime('%Y-%m-%d')


def parse_csv_line(line: str) -> List[str]:
    """
    Parse a CSV line, handling quoted fields.
    
    Args:
        line: CSV line to parse
        
    Returns:
        List[str]: List of fields
    """
    fields = []
    current_field = ""
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                # Escaped quote
                current_field += '"'
                i += 1
            else:
                # Toggle quote state
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            # Field separator
            fields.append(current_field.strip())
            current_field = ""
        else:
            current_field += char
        
        i += 1
    
    # Add the last field
    fields.append(current_field.strip())
    
    return fields


def validate_csv_data(data: List[List[str]], expected_columns: int) -> Tuple[bool, str]:
    """
    Validate CSV data format.
    
    Args:
        data: List of CSV rows
        expected_columns: Expected number of columns
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not data:
        return False, "CSV file is empty"
    
    for i, row in enumerate(data):
        if len(row) != expected_columns:
            return False, f"Row {i + 1} has {len(row)} columns, expected {expected_columns}"
    
    return True, ""


def get_color_for_percentage(percentage: float) -> str:
    """
    Get a color name based on percentage value.
    
    Args:
        percentage: Percentage value (0-100)
        
    Returns:
        str: Color name for display
    """
    if percentage >= 100:
        return "red"  # Over budget
    elif percentage >= 80:
        return "yellow"  # Warning
    elif percentage >= 50:
        return "blue"  # Moderate
    else:
        return "green"  # Good


def format_time_elapsed(start_time: datetime, end_time: Optional[datetime] = None) -> str:
    """
    Format elapsed time between two datetime objects.
    
    Args:
        start_time: Start datetime
        end_time: End datetime (defaults to now)
        
    Returns:
        str: Formatted elapsed time
    """
    if end_time is None:
        end_time = datetime.now()
    
    elapsed = end_time - start_time
    total_seconds = int(elapsed.total_seconds())
    
    if total_seconds < 60:
        return f"{total_seconds}s"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}m {seconds}s"
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"


# TODO: Add multi-month comparison charts for spending trends
# TODO: Add category heatmaps in reports
# TODO: Add goal completion notifications (console or email)
# TODO: Fix bug: totals sometimes miscalculate if income added before budget setup
# TODO: Add export to CSV/XLSX option
# TODO: Add dark mode support for charts
# TODO: Implement unit tests for budget and goal modules
