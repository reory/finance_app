# Analytics - summarisation of data for dashboards and reports.

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models import Q
from apps.analytics.models import Transaction
from itertools import accumulate
from datetime import date


def get_monthly_income_expense(user):
    """
    Returns:
    [
        {"month": datetime, "income": Decimal, "expenses": Decimal},
        ...
    ]
    """

    qs = (
        Transaction.objects
        .filter(user=user)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            income=Sum("amount", filter=Q(amount__gt=0)),
            expenses=Sum("amount", filter=Q(amount__lt=0)),
        )
        .order_by("month")
    )

    # Replace None with 0 for months missing income or expenses
    result = []
    for row in qs:
        result.append({
            "month": row["month"],
            "income": row["income"] or 0,
            "expenses": row["expenses"] or 0,
        })

    return result


def get_category_breakdown(user):
    """
    Returns:
    [
        {"category": "Food", "total": Decimal},
        {"category": "Bills", "total": Decimal},
        ...
    ]
    """
    
    # Sum amounts by category
    qs = (
        Transaction.objects
        .filter(user=user)
        .values("category")                  # Group by category
        .annotate(total=Sum("amount"))       # Sum amounts
        .order_by("-total")                  # Higest to the lowest
    )

    return list(qs)

def get_income_expense_summary(user):
    """
    Returns:
    {
        "income": Decimal,
        "expenses": Decimal
    }
    """
    
    qs = Transaction.objects.filter(user=user)
    
    # Sum all positive amounts
    income = (qs.filter(
        amount__gt=0).aggregate(
        total=Sum("amount"))["total"] or 0
    )
    # Sum all negative amounts
    expenses = (qs.filter(
        amount__lt=0).aggregate(
        total=Sum("amount"))["total"] or 0
    )

    return {
        "income": income,
        "expenses": expenses,
    }

def get_running_balance(user):
    """
    Returns:
    [
        {"date": date, "balance": Decimal},
        ...
    ]
    """
    # Get transactions ordered by date
    qs = (
        Transaction.objects
        .filter(user=user)
        .order_by("date")
        .values("date", "amount")
    )
    
    # Extract amounts for cumulative sum
    amounts = [row["amount"] for row in qs]
    balances = list(accumulate(amounts))       # Running total
    
    # Pair each date with its running balance
    result = []
    for row, balance in zip(qs, balances):
        result.append({
            "date": row["date"],
            "balance": balance,
        })

    return result

def get_transactions_in_range(user, start: date, end: date):
    """Returns all transactions between start and end dates."""
    
    # Filter by date range
    qs = (
        Transaction.objects
        .filter(user=user, date__gte=start, date__lte=end)
        .order_by("date")
    )

    return list(qs.values())

