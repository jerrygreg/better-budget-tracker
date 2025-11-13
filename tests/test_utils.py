import pytest
from utils import (
    validate_amount,
    parse_amount,
    format_currency,
    validate_date,
    format_date,
)


def test_validate_amount_string_valid():
    assert validate_amount("$3,500.75") is True


def test_validate_amount_string_invalid():
    assert validate_amount("300 hundred dollars") is False


def test_validate_amount_int_valid():
    assert validate_amount(3500) is True


def test_validate_amount_int_invalid():
    assert validate_amount(-3500) is False


def test_validate_amount_type_invalid():
    assert validate_amount([300, 2500]) is False


def test_parse_amount_string_valid():
    assert parse_amount("$3,500.75") == 3500.75


def test_parse_amount_string_empty():
    with pytest.raises(ValueError) as e:
        parse_amount("")
    assert "Amount cannot be empty" in str(e.value)


def test_parse_amount_string_invalid():
    with pytest.raises(ValueError) as e:
        parse_amount("$3.500.75")
    assert "Invalid amount format: $3.500.75" in str(e.value)


def test_format_currency_default():
    assert format_currency(150.5) == "₹150.50"


def test_format_currency_pound_sterling():
    assert format_currency(150.5, "£") == "£150.50"


def test_format_currency_dollar():
    assert format_currency(150, "$") == "$150.00"


def test_validate_date_date_string_empty():
    assert validate_date("") is False


def test_validate_date_date_string_valid():
    assert validate_date("2025-10-30") is True


def test_validate_date_date_string_format_invalid():
    assert validate_date("30-10-2025") is False


def test_validate_date_date_string_date_invalid():
    assert validate_date("2025-13-30") is False


def test_format_date_date_string_valid_default_formats():
    assert format_date("2025-10-30") == "October 30, 2025"


def test_format_date_date_string_valid_alternate_formats():
    assert format_date("30-10-2025", "%d-%m-%Y", "%Y-%m-%d") == "2025-10-30"


def test_format_date_date_string_invalid_date_format():
    test_date_string = "2025-10-30"
    test_input_format = "%d-%m-%Y"
    with pytest.raises(ValueError) as e:
        format_date(test_date_string, test_input_format, "%Y-%m-%d")
    assert (
        f"Invalid date format: time data '{test_date_string}' does "
        f"not match format '{test_input_format}'"
    ) in str(e.value)
