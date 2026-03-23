"""
Summarizer module:
Produces aggregated summaries from normalized + categorized transactions.
"""

from collections import defaultdict
from datetime import datetime


class Summarizer:

    @classmethod
    def monthly_totals(cls, transactions):
        """
        Returns:
        [
            {"month": "2024-01", "total": 123.45},
            {"month": "2024-02", "total": 98.10},
            ...
        ]
        """

        totals = defaultdict(float)

        for tx in transactions:
            date_str = tx.get("date", "")
            month = cls._extract_month(date_str)
            amount = float(tx.get("amount", 0))
            totals[month] += amount

        return [{"month": m, "total": t} for m, t in sorted(totals.items())]

    @classmethod
    def category_breakdown(cls, transactions):
        """
        Returns:
        [
            {"category": "food", "total": 50.00},
            {"category": "transport", "total": 20.00},
            ...
        ]
        """

        totals = defaultdict(float)

        for tx in transactions:
            category = tx.get("category", "other")
            amount = float(tx.get("amount", 0))
            totals[category] += amount

        return [{
            "category": c, 
            "total": t} for c, t in sorted(totals.items(), key=lambda x: -x[1])]

    @classmethod
    def income_expense(cls, transactions):
        """
        Returns:
        {
            "income": float,
            "expenses": float
        }
        """

        income = 0.0
        expenses = 0.0

        for tx in transactions:
            amount = float(tx.get("amount", 0))
            if amount > 0:
                income += amount
            else:
                expenses += amount

        return {"income": income, "expenses": expenses}

    @classmethod
    def running_balance(cls, transactions):
        """
        Returns:
        [
            {"date": "2024-01-01", "balance": 100.00},
            {"date": "2024-01-02", "balance": 120.00},
            ...
        ]
        """

        # Sort by date
        sorted_tx = sorted(transactions, key=lambda x: x.get("date", ""))

        balance = 0.0
        result = []

        for tx in sorted_tx:
            amount = float(tx.get("amount", 0))
            balance += amount
            result.append({
                "date": tx.get("date", ""),
                "balance": balance
            })

        return result

    @staticmethod
    def _extract_month(date_str):
        """Convert YYYY-MM-DD → YYYY-MM."""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m")
        except Exception:
            return "unknown"
        
    @classmethod
    def generate(cls, transactions):
        """
        Produce a full summary bundle for dashboards or reports.
        """
        return {
            "monthly_totals": cls.monthly_totals(transactions),
            "category_breakdown": cls.category_breakdown(transactions),
            "income_expense": cls.income_expense(transactions),
            "running_balance": cls.running_balance(transactions),
        }

