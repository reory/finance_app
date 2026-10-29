from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Transaction


@login_required
def dashboard_view(request):
    """Renders the main finance analytics dashboard."""

    transaction_count = Transaction.objects.filter(user=request.user).count()

    context = {
        "transaction_count": transaction_count,
    }
    return render(request, "dashboard.html", context)


@login_required
def status_view(request):
    """Renders the status view."""

    return render(request, "status.html")


@login_required
def transactions_view(request):
    """Display and manage user transactions."""

    transactions = Transaction.objects.filter(user=request.user)
    return render(
        request, "analytics/transactions.html", {"transactions": transactions}
    )


@login_required
@require_POST
def clear_transactions(request):
    """Deletes all transactions for the current user."""

    Transaction.objects.filter(user=request.user).delete()
    messages.success(request, "All transactions have been cleared.")
    return redirect("analytics:transactions")


