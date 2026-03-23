# backend/apps/analytics/services/csv_cleaner.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class CleanResult:
    cleaned_rows: List[Dict[str, Any]]
    errors: List[str]


class CSVCleaner:
    """
    Cleaner for analytics pipeline.
    Collect errors for reporting/logging
    """

    # Common date formats we’ll try in order
    DATE_FORMATS = [
        "%Y-%m-%d",   # 2024-01-02
        "%d/%m/%Y",   # 01/02/2024
        "%Y/%m/%d",   # 2024/01/02
        "%d-%m-%Y",   # 01-02-2024
        "%d-%m-%y",   # 01-02-24
        "%d %b %Y",   # 1 Jan 2024
        "%b %d %Y",   # Jan 1 2024
    ]

    REQUIRED_FIELDS = ["date", "description", "amount"]

    @classmethod
    def clean_rows(cls, rows: List[Dict[str, Any]]) -> CleanResult:
        """
        Main entrypoint.

        - Takes raw DictReader rows
        - Cleans each row
        - Skips invalid ones
        - Returns CleanResult(cleaned_rows, errors)
        """
        cleaned: List[Dict[str, Any]] = []
        errors: List[str] = []

        for idx, row in enumerate(rows, start=1):
            # Skip completely empty rows
            if not row or all((
                v is None or str(v).strip() == "") for v in row.values()):
                continue

            # Skip comment-like rows (first non-empty value starts with #)
            first_val = next((
                str(v).strip() for v in row.values() if str(v).strip()), "")
            if first_val.startswith("#"):
                continue

            # Skip duplicate header rows 
            # (e.g."date,description,category,amount")
            lower_vals = [
                str(v).lower().strip()
                for v in row.values() 
                if v is not None and str(v).strip() != ""
            ]

            if (
                "date" in lower_vals 
                and "description" in lower_vals 
                and "amount" in lower_vals
            ):
                # Looks like a header repeated as a row
                continue

            try:
                cleaned_row = cls._clean_single_row(row)
                cleaned.append(cleaned_row)
            except ValueError as e:
                errors.append(f"Row {idx}: {e}")

        return CleanResult(cleaned_rows=cleaned, errors=errors)

    @classmethod
    def _clean_single_row(cls, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean a single row.

        - Normalises keys to lower-case for internal handling
        - Extracts and cleans date, description, amount, category
        - Raises ValueError if row is unusable
        """
        # Normalise keys (but keep original dict intact for safety)
        # If header is None convert it to a empty string
        # Lower() is always called on a string
        normalised = {
            (str(k).lower().strip() if k is not None else ""): v
             for k, v in row.items()
        }

        # Basic required fields presence check (by common names)
        date_raw = cls._get_first(normalised, [
            "date", "transaction_date", "posted", "day"])
        desc_raw = cls._get_first(normalised, [
            "description", "desc", "merchant", "details", "narrative"])
        amount_raw = cls._get_first(normalised, [
            "amount", "value", "amt", "transaction_amount"])
        category_raw = cls._get_first(normalised, [
            "category", "type", "group"])

        if not date_raw or not str(date_raw).strip():
            raise ValueError("Missing date")
        if not desc_raw or not str(desc_raw).strip():
            raise ValueError("Missing description")
        if not amount_raw or not str(amount_raw).strip():
            raise ValueError("Missing amount")

        cleaned_date = cls._clean_date(str(date_raw))
        if cleaned_date is None:
            raise ValueError(f"Invalid date format: {date_raw!r}")

        cleaned_amount = cls._clean_amount(str(amount_raw))
        if cleaned_amount is None:
            raise ValueError(f"Invalid amount: {amount_raw!r}")

        cleaned_category = cls._clean_category(
            str(category_raw) 
            if category_raw is not None else "")

        return {
            "date": cleaned_date,          # ISO string YYYY-MM-DD
            "description": str(desc_raw).strip(),
            "amount": cleaned_amount,      # float
            "category": cleaned_category,  # normalised string
        }

    @staticmethod
    def _get_first(row: Dict[str, Any], keys: List[str]) -> Optional[Any]:
        for key in keys:
            if key in row:
                return row[key]
        return None

    @classmethod
    def _clean_date(cls, value: str) -> Optional[str]:
        """
        Try multiple date formats and return ISO string (YYYY-MM-DD),
        or None if all formats fail.
        """
        value = value.strip()

        # Quick guard for obviously bad values
        if not value or value.lower() in {"n/a", "na", "none", "null"}:
            return None

        for fmt in cls.DATE_FORMATS:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.date().isoformat()
            except ValueError:
                continue

        return None

    @classmethod
    def _clean_amount(cls, value: str) -> Optional[float]:
        """
        Clean messy amount strings into a float.

        Handles:
        - currency symbols (e.g. £, $, €)
        - commas (e.g. 2,500.00)
        - negative in brackets (e.g. (850))
        - spaces around minus (e.g. - 48.10)
        - trailing comments (we stop at first non-number-ish chunk)
        """
        original = value
        value = value.strip()

        if not value or value.lower() in {"n/a", "na", "none", "null"}:
            return None

        # Handle bracket negatives: (850) -> -850
        is_negative = False
        if value.startswith("(") and value.endswith(")"):
            is_negative = True
            value = value[1:-1].strip()

        # Remove currency symbols and other obvious non-numeric prefixes
        # Keep digits, minus, dot, comma, and space
        cleaned_chars = []
        for ch in value:
            if ch.isdigit() or ch in "-., ":
                cleaned_chars.append(ch)
            else:
                # Stop at first clearly non-numeric-ish char (e.g. '#', letters)
                break
        value = "".join(cleaned_chars).strip()

        # Remove spaces around minus
        value = value.replace(" -", "-").replace("- ", "-")

        # Remove commas (thousands separators)
        value = value.replace(",", "")

        if not value:
            return None

        try:
            num = float(value)
        except ValueError:
            return None

        if is_negative and num > 0:
            num = -num

        return num

    @staticmethod
    def _clean_category(value: str) -> str:
        """
        Normalise category:
        - trim
        - title-case
        - fix common typos
        - default to 'Uncategorised' if empty
        """
        value = value.strip()

        if not value:
            return "Uncategorised"

        # Normalise spacing and casing
        norm = " ".join(value.split()).title()

        # Fix a few common typos
        fixes = {
            "Utilties": "Utilities",
            "Utitlities": "Utilities",
            "Restuarant": "Restaurant",
        }
        norm = fixes.get(norm, norm)

        return norm or "Uncategorised"
