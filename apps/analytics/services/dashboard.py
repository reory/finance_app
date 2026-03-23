# High‑level analytics providers for dashboards and API responses
from apps.analytics.services.db_summarizer import (
       get_monthly_income_expense,
       get_category_breakdown,
       get_income_expense_summary,
       get_running_balance,
       get_transactions_in_range,
)

def dashboard_monthly_overview(user):
        """Return monthly totals in a UI structure."""

        data = get_monthly_income_expense(user)

        return {
            "monthly_totals": data,               # List of {month, totals}
            "count": len(data)                    # Number of months returned
        }

def dashboard_category_overview(user):
        """Return category totals for charts or tables."""

        data = get_category_breakdown(user)

        return {
            "categories": data,                   # List of {category, total}
            "count": len(data)                    # Number of categories
        }

def dashboard_income_expenses(user):
        """Return income vs expense summary."""

        summary = get_income_expense_summary(user)

        return {
            "income": summary["income"],                  # Total positive amounts
            "expenses": summary["expenses"],              # Total negative amounts
            "net": summary["income"] + summary["expenses"],          # Net balance
        }

def dashboard_running_balance(user):
        """Return running balance for line charts/etc."""

        data = get_running_balance(user)

        return {
            "running_balance": data,             # List of {date, balance}
            "count": len(data),                  # Number of results
        }

def dashboard_transactions_in_range(user, start, end):
    """Return all transactions in a date range."""

    data = get_transactions_in_range(user, start, end)

    return {
           "transactions": data,                # List of transactions in range
           "count": len(data),                  # Number of results
           "start": start,                      # Show the range start
           "end": end,                          # Show the range end                   
        }