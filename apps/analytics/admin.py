from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    # Columns shown in the admin list view
    list_display = ("id", "user", "category", "amount", "date")

    # Search bar fields
    search_fields = ("user__username", "category", "description")

    # Right side filters
    list_filter = ("category", "date")

    # Order newest first - (must be a list or tuple.)
    ordering = ["-date",]