from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfilAdmin(admin.ModelAdmin):
    """Admin configuration for managing UserProfile records in the Django admin site."""

    # Columns shown in the admin list view
    list_display = ("user", "organisation", "timezone", "onboarding_complete")

    # Search bar fields
    search_fields = ("user__username", "organisation")

    # Right side filters
    list_filter = ("timezone", "onboarding_complete")
