# Data model for recording how donations are allocated to different beneficiaries
# Supports audit trails for transparency and compliance

from django.db import models
from simple_history.models import HistoricalRecords

class Allocation(models.Model):
    # name of beneficiary organisation or cause
    beneficiary_name = models.CharField(max_length=255)

    # percentage of the total donation assigned to this beneficiary
    percent = models.DecimalField(max_digits=5, decimal_places=2)

    # monetary amount corresponding to the allocation
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # timestamp automatically added when the record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # enables automatic version tracking for full audit history
    history = HistoricalRecords() 

    def __str__(self):
        return f"{self.beneficiary_name} ({self.percent}%)"
