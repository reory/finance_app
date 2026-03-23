"""
Normalizer module:
Standardizes field formats (dates, amounts, text) for consistent downstream processing.
"""

from datetime import datetime


class Normalizer:

    @classmethod
    def normalize(cls, transactions):
        """
        Normalize a list of transaction dicts.
        - Convert dates to ISO format
        - Convert amounts to float
        - Lowercase descriptions
        - Strip whitespace
        """

        normalized = []

        for tx in transactions:
            normalized_tx = cls._normalize_single(tx)
            normalized.append(normalized_tx)

        return normalized

    @classmethod
    def _normalize_single(cls, tx):
        """Normalize a single transaction dict."""

        # Normalize date
        tx["date"] = cls._normalize_date(tx.get("date"))

        # Normalize amount
        tx["amount"] = cls._normalize_amount(tx.get("amount"))

        # Normalize description
        desc = tx.get("description", "")
        tx["description"] = desc.strip().lower()

        return tx

    @staticmethod
    def _normalize_date(value):
        """Convert various date formats to YYYY-MM-DD."""

        if not value:
            return ""

        # Already ISO
        try:
            return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
        except ValueError:
            pass

        # Common UK format: DD/MM/YYYY
        try:
            return datetime.strptime(value, "%d/%m/%Y").date().isoformat()
        except ValueError:
            pass

        # Common US format: MM/DD/YYYY
        try:
            return datetime.strptime(value, "%m/%d/%Y").date().isoformat()
        except ValueError:
            pass

        # Fallback: return raw
        return value

    @staticmethod
    def _normalize_amount(value):
        """Convert amount to float, stripping currency symbols."""

        if value is None:
            return 0.0

        if isinstance(value, (int, float)):
            return float(value)

        # Remove currency symbols and commas
        cleaned = (
            str(value)
            .replace(",", "")
            .replace("£", "")
            .replace("$", "")
            .strip()
        )

        try:
            return float(cleaned)
        except ValueError:
            return 0.0
