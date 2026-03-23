# CRUD
from django.urls import path
from .views import (
    transactions_view, create_transaction, update_transaction,
    delete_transaction, dashboard_view, dashboard_range_view,
    upload_transactions, charts_views
)

app_name = "analytics"

urlpatterns = [
    # /analytics/transactions/ | Shows the logged in users transactions
    path("transactions/", transactions_view, name="transactions"),
    
    # Create new transaction
    path("transactions/create/", create_transaction, name="transaction_create"),

    # Edit an existing transaction - user owned only
    path("transactions/<int:pk>/edit/", update_transaction, 
        name="transaction_edit"
    ),

    # Delete an existing transaction - user owned only
    path("transaction/<int:pk>/delete/", delete_transaction, 
        name="transaction_delete"
    ),

    # Dashboard main view
    path("dashboard/", dashboard_view, name="dashboard"),

    # Dashboard date-range analytics
    path("dashboard/range/", dashboard_range_view, name="dashboard_range"),
    
    # Upload the CSV view
    path("upload/", upload_transactions, name="upload"),

    # Charts data
    path("charts/", charts_views, name="charts"),

]