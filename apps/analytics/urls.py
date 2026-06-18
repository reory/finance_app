from django.urls import path, include
from . import views

app_name = "analytics"

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("transactions/", views.transactions_view, name="transactions"),
    path("uploads/", include("apps.uploads.urls")),
    path("status/", views.status_view, name="status"),
]
