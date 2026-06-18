from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction


@login_required
def dashboard_view(request):
    """Renders the main finance analytics dashboard."""

    return render(request, "dashboard.html")


@login_required
def status_view(request):
    """Renders the status view."""

    return render(request, "status.html")


@login_required
def transactions_view(request):

    transactions = Transaction.objects.filter(user=request.user)
    return render(
        request, "analytics/transactions.html", {"transactions": transactions}
    )
