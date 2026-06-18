from django.urls import path
from . import views

app_name = "uploads"

urlpatterns = [
    path("csv/", views.upload_view, name="upload"),
]
