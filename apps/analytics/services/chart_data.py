from apps.analytics.services.db_summarizer import get_monthly_income_expense

def get_chart_data(user):
    summary = get_monthly_income_expense(user)

    labels = []
    income = []
    expenses = []

    for row in summary:
        labels.append(row["month"].strftime("%b %Y"))
        income.append(float(row["income"]))
        expenses.append(float(row["expenses"]))

    return {
        "labels": labels,
        "income": income,
        "expenses": expenses,
    }
