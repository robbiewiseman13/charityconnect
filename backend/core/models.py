# Database model definitions for the core app
# Defines how donation data is stored, managed, and audited within the CharityConnect system

from django.db import models
from simple_history.models import HistoricalRecords

class Donation(models.Model):
    # donors full name
    donor_name = models.CharField(max_length=100)

    # donation amount in euro
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # timestamp automatically added when the record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # enables audit trail for all changes for transparency and complaince
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.donor_name} donated €{self.amount}"
