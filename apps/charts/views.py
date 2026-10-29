from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.analytics.models import Transaction


@login_required
def charts_view(request):
    """Display charts and visualizations for the application."""

    # Fetch  all transactions for the user ordered by date
    transactions = Transaction.objects.filter(user=request.user).order_by("date")


    # Aggregate income (Credits) and expenses (Debits) by month
    monthly_dict = {}

    for tx in transactions:
        # Group by Month and Year
        m_str = tx.date.strftime("%b %Y")

        if m_str not in monthly_dict:
            monthly_dict[m_str] = {
                "sort_date": tx.date.replace(day=1), 
                "Income": 0.0, 
                "Expenses": 0.0
            }
        val = float(tx.amount or 0)
        if tx.type == "Credit" or val > 0:
            monthly_dict[m_str]["Income"] += val
        elif tx.type == "Debit" or val < 0:
            # Ensure expenses are positive on the chart
            monthly_dict[m_str]["Expenses"] += abs(val)

    # Sort months chronologically based on their actual date
    sorted_months = sorted(monthly_dict.values(), key=lambda x: x["sort_date"])

    months = [item["sort_date"].strftime("%b %Y") for item in sorted_months]
    incomes = [item["Income"] for item in sorted_months]
    expenses = [item["Expenses"] for item in sorted_months]
    

    # Generate the insight message based on the last recorded month
    insight = ""
    if sorted_months:
        last_month = sorted_months[-1]
        last_month_name = last_month["sort_date"].strftime("%B")
        if last_month["Income"] > last_month["Expenses"]:
            insight = f"Your income exceeded your expenses in {last_month_name}."
        else:
            insight = f"Your expenses exceeded your income in {last_month_name}."

    context = {
        "months": months,
        "incomes": incomes,
        "expenses": expenses,
        "insight": insight,
    }

    return render(request, "charts/charts.html", context)
