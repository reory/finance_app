# This stores uploaded CSVs so users can re‑import or audit later.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UploadedFile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to="uploads/csv/")
    uploaded_at = models. DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.file.name}"