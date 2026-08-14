# Project level urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("analytics/", include("apps.analytics.urls")),
    path("accounts/", include("accounts.urls")),
    path("uploads/", include("apps.uploads.urls")),
    path("charts/", include("apps.charts.urls")),
    path("", include("accounts.urls")),
]
