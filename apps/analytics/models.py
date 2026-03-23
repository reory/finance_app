from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    
    # Every transcation belongs to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Stores the transaction date
    date = models.DateField()
    # Text describing the transaction
    description = models.CharField(max_length=155)
    # Category labels - eg. food/bills/etc
    category = models.CharField(max_length=100)
    # Financial values eg. 24.00/330.55
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # This is sorting, analytics and audit trails.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.description} - {self.amount}"