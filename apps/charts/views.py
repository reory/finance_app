from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Sum, Value
from django.db.models.functions import TruncMonth, Coalesce
from apps.analytics.models import Transaction


@login_required
def charts_view(request):
    # We explicitly tell Django that the output must be a DecimalField
    data = (
        Transaction.objects.filter(user=request.user)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            total_income=Coalesce(
                Sum("amount", filter=models.Q(type="Income")),
                Value(0),
                output_field=models.DecimalField(),
            ),
            total_expenses=Coalesce(
                Sum("amount", filter=models.Q(type="Expense")),
                Value(0),
                output_field=models.DecimalField(),
            ),
        )
        .order_by("month")
    )

    # Prepare data for chart.js
    months = [d["month"].strftime("%b %Y") for d in data]
    incomes = [float(d["total_income"]) for d in data]
    expenses = [float(d["total_expenses"]) for d in data]

    # Generate the insight message
    last_month = data.last()
    insight = ""
    if last_month:
        if (last_month["total_income"] or 0) > (last_month["total_expenses"] or 0):
            insight = f"Your income exceeded your expenses in {last_month['month'].strftime('%B')}."
        else:
            insight = f"Your expenses exceeded your income in {last_month['month'].strftime('%B')}."

    context = {
        "months": months,
        "incomes": incomes,
        "expenses": expenses,
        "insight": insight,
    }

    return render(request, "charts/charts.html", context)
