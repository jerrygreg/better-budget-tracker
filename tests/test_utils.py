import pytest
from utils import validate_amount, parse_amount


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


