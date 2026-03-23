from django import forms
from .models import Transaction

# This manages validation and ensures the user field is never exposed.
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # User is assigned automatically
        exclude = ("user",)