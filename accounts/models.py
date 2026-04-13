from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    # Multi tenant support
    organisation = models.CharField(max_length=100, blank=True, null=True)
    # User preferences - personalise dashboards, reports and scheduling
    timezone = models.CharField(max_length=50, default="UTC")
    # Onboarding flow guided support
    onboarding_complete = models.BooleanField(default=False)

    def __str__(self):
        """Make admin page readable."""
        return self.user.username
