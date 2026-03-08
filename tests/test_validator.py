from utils.validator import Validator


def test_validate_phone_accepts_valid_international_numbers() -> None:
    assert Validator.validate_phone("+380501234567") is True  # Ukraine
    assert Validator.validate_phone("+123456789012") is True  # US
    assert Validator.validate_phone("+442012345678") is True  # UK
    assert Validator.validate_phone("+491234567890") is True  # Germany
    assert Validator.validate_phone("+15551234567") is True  # US short


def test_validate_phone_rejects_invalid_numbers() -> None:
    assert Validator.validate_phone("380501234567") is False  # missing +
    assert Validator.validate_phone("+123456") is False  # too short (< 7 digits)
    assert (
        Validator.validate_phone("+080501234567") is False
    )  # country code cannot start with 0
    assert Validator.validate_phone("+12345") is False  # too short
    assert (
        Validator.validate_phone("+12345678901234567") is False
    )  # too long (> 15 digits)


def test_validate_email_accepts_common_formats() -> None:
    assert Validator.validate_email("user@example.com") is True
    assert Validator.validate_email("user.name-1@test.co.ua") is True


def test_validate_email_rejects_invalid_formats() -> None:
    assert Validator.validate_email("invalid-email") is False
    assert Validator.validate_email("user@") is False
    assert Validator.validate_email("@example.com") is False


def test_validate_date_accepts_year_month_day_patterns() -> None:
    # Підходять як одно-, так і двозначні місяці/дні
    assert Validator.validate_date("2024-1-1") is True
    assert Validator.validate_date("2024-12-31") is True


def test_validate_date_rejects_wrong_pattern() -> None:
    assert Validator.validate_date("2024/01/01") is False
    assert Validator.validate_date("01-01-2024") is False
    assert Validator.validate_date("2024-001-01") is False


def test_validate_days_checks_digits_only() -> None:
    assert Validator.validate_days("0") is True
    assert Validator.validate_days("10") is True
    assert Validator.validate_days("001") is True
    assert Validator.validate_days("") is False
    assert Validator.validate_days("ten") is False
    assert Validator.validate_days("10days") is False


def test_validate_search_term_empty_term_matches_any() -> None:
    assert Validator.validate_search_term("anything", "") is True


def test_validate_search_term_substring_case_insensitive() -> None:
    assert Validator.validate_search_term("Alice", "alice") is True
    assert Validator.validate_search_term("bob@example.com", "example") is True
    assert Validator.validate_search_term("Alice", "x") is False


def test_validate_search_term_wildcard_default() -> None:
    assert Validator.validate_search_term("Alice", "*ice") is True
    assert Validator.validate_search_term("Alice", "Ali*") is True
    assert Validator.validate_search_term("Second important", "*ond*") is True
    assert Validator.validate_search_term("Bob", "*ice") is False


def test_validate_search_term_wildcard_parameterized() -> None:
    # інший символ wildcard
    assert Validator.validate_search_term("hello", "he%o", wildcard="%") is True
    assert Validator.validate_search_term("hello", "he*o", wildcard="%") is False
