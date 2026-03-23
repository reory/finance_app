# Part of the analytics domain
# Fits in with the transaction model

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# Django built in system for showing info messages to the user.
from django.contrib import messages

from apps.analytics.models import Transaction

from .forms import TransactionForm

from apps.pipeline.engine.convertor import extract_csv_rows
from apps.analytics.importers.csv_importer import process_csv_rows
from apps.analytics.services.dashboard import (
    dashboard_monthly_overview,
    dashboard_category_overview,
    dashboard_income_expenses,
    dashboard_running_balance,
    dashboard_transactions_in_range,

)
from apps.analytics.services.csv_cleaner import CSVCleaner

from apps.logs.analytics_logger import (
    log_dashboard_access, 
    log_analytics_error,
)
from apps.logs.pipeline_logger import log_pipeline_step, log_pipeline_error
from apps.analytics.services.chart_data import get_chart_data

@login_required
def transactions_view(request):
    
    # Logs every time a user opens the transaction page
    log_pipeline_step("Transactions list viewed")
    
    # Only return transactions that belong to the logged in user.
    transactions = Transaction.objects.filter(user=request.user)

    # Pass the filtered transactions to the template HTML
    return render(
        request, "analytics/transactions.html", {"transactions": transactions})

@login_required
def upload_transactions(request): 
    
    # CSV VIEW
    # This gives you: “CSV upload started” “CSV extraction error” 
    # “CSV processing errors” “CSV import complete”

    if request.method == "POST":
        log_pipeline_step("CSV upload started")
        rows, error = extract_csv_rows(request.FILES.get("file"))

        if error:
            log_pipeline_error(f"CSV extraction error: {error}")
            messages.error(request, error)
            return redirect("analytics:transactions")
        
        if rows is None:
            messages.error(request, "CSV extraction failed.")
            return redirect("analytics:transactions")
        
        # Updated cleaner layer for deeper cleaning and fxixing of CSV files
        clean_result = CSVCleaner.clean_rows(rows)
        cleaned_rows = clean_result.cleaned_rows
        clean_errors = clean_result.errors

        # Log skipped and bad rows
        if clean_errors:
            log_pipeline_error(f"CSV cleaning skipped rows: {clean_errors}")
            messages.warning(
                request,
                f"Some rows were skipped during cleaning: " 
                f"Please investigate: {clean_errors}"
        )
        
        # Pass only clean rows into the exisitng pipeline
        errors, imported_count = process_csv_rows(cleaned_rows,request.user)

        if errors:
            log_pipeline_error(f"CSV processing errors: {errors}")
            messages.error(request, f"Errors found: {errors}")
        else:
            log_pipeline_step(f"CSV import complete: {imported_count} rows")
            messages.success(request, f"Imported {imported_count} transactions.")

        return redirect("analytics:transactions")
    
    
    return render(request, "analytics/upload_form.html")

@login_required
def create_transaction(request):

    if request.method == "POST":
        log_pipeline_step("Transaction created")
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)

            # Enforce mulit-tenant ownership
            transaction.user = request.user
            transaction.save()

            # Redirect back to the list view
            return redirect("transactions")
    else:
        form = TransactionForm()

        # Template for transactions
    return render(request, "analytics/transaction_form.html", {"form": form})

@login_required
def update_transaction(request, pk):

    

    # Only allow editing of the logged in users transactions
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == "POST":
        log_pipeline_step(f"Transaction {pk} updated")
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()

            return redirect("transactions")
        
    else:
        form = TransactionForm(instance=transaction)

    # template placeholder for now
    return render(request, "analytics/transaction_form.html", {"form": form})

@login_required
def delete_transaction(request, pk):

    # Only allow deletion of the logged in users transaction/s
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    # Log deletion
    log_pipeline_step(f"Transaction {pk} deleted")

    transaction.delete()
    return redirect("transactions")


@login_required
def dashboard_view(request):
    """Collect all analytics data for the dashboard."""
    
    # Log dashboard load
    # A log entry every time a user loads the dashboard
    # Error logging if analytics fail
    log_dashboard_access(request.user)
    
    try:
        monthly = dashboard_monthly_overview(request.user)
        categories = dashboard_category_overview(request.user)
        income_expenses = dashboard_income_expenses(request.user)
        running = dashboard_running_balance(request.user)
    except Exception as e:
        log_analytics_error(str(e))
        raise

    context = {
        "monthly": monthly,
        "categories": categories,
        "income_expenses": income_expenses,
        "running": running,
    }

    # Placeholder template for now
    return render(request, "analytics/dashboard.html", context)

@login_required
def dashboard_range_view(request):
    """Analytics for a custom date range."""

    # Dashboard range access
    log_dashboard_access(request.user)

    start = request.GET.get("start")
    end = request.GET.get("end")

    if not start or not end:

        # This gives you visibility into user mistakes.
        log_analytics_error("Dashboard range missing start or end date")
        messages.error(request, "Start and end dates are required.")
        return redirect("analytics:dashboard")
    
    # Log range analytics
    log_pipeline_step(f"Dashboard range analytics: {start} -> {end}")

    data = dashboard_transactions_in_range(request.user, start, end)

    return render(request, "analytics/dashboard_range.html", {"range_data": data})

@login_required
def charts_views(request):
    """Render the chart data using chart.js"""

    data = get_chart_data(request.user)
    return render(request, "analytics/charts.html", {"chart_data": data})






