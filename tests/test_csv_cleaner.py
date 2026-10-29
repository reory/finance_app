# tests/pipeline/test_csv_cleaner.py

from decimal import Decimal

from apps.pipeline.csv_cleaner import (
    clean_amount,
    clean_csv_content,
    parse_date,
)


def test_clean_amount_parses_currency():
    """Currency symbols and commas are stripped correctly."""

    value, txn_type = clean_amount("£2,500.00")

    assert value == Decimal("2500.00")
    assert txn_type == "Credit"


def test_clean_amount_parses_negative_accounting_value():
    """Accounting-style values in parentheses become negative debits."""

    value, txn_type = clean_amount("(850)")

    assert value == Decimal(-850)
    assert txn_type == "Debit"


def test_clean_amount_expense_becomes_debit():
    """Expense transaction types are converted to negative debit amounts."""

    value, txn_type = clean_amount("100", "Expense")

    assert value == Decimal(-100)
    assert txn_type == "Debit"


def test_clean_amount_invalid_value():
    """Invalid numeric values return None instead of raising exceptions."""

    assert clean_amount("banana") == (None, None)


def test_parse_date_common_format():
    """Standard ISO dates are parsed correctly."""

    result = parse_date("2024-01-15")

    assert result.isoformat() == "2024-01-15"


def test_parse_date_invalid():
    """Invalid date strings return None."""

    assert parse_date("not-a-date") is None


def test_clean_csv_valid_transaction():
    """A valid CSV row is transformed into a cleaned transaction record."""

    csv_data = b"""
    Date,Description,Category,Amount
    2024-01-15,Coffee,Food,-4.50
    """

    valid_rows, skipped_rows = clean_csv_content(csv_data)

    assert skipped_rows == []
    assert len(valid_rows) == 1

    row = valid_rows[0]

    assert row["description"] == "Coffee"
    assert row["category"] == "Food"
    assert row["amount"] == Decimal("-4.50")
    assert row["type"] == "Debit"


def test_clean_csv_skips_invalid_rows():
    """Rows with invalid dates or amounts are skipped and recorded."""

    csv_data = b"""
    Date,Description,Category,Amount
    bad-date,Coffee,Food,-4.50
    2024-01-15,Lunch,Food,banana
    """

    valid_rows, skipped_rows = clean_csv_content(csv_data)

    assert valid_rows == []
    assert len(skipped_rows) == 2