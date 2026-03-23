from django.urls import path
from .views import upload_csv, upload_result

app_name="uploads"

urlpatterns = [
    path("upload/", upload_csv, name="upload_csv"),
    path("result/", upload_result, name="result"),
]
