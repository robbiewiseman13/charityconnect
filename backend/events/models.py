from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from charities.models import Charity

class Event(models.Model):
    organiser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='events'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    venue = models.CharField(max_length=200, blank=True)
    base_ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    published = models.BooleanField(default=False)

    def clean(self):
        # Only enforce rules when publishing
        if self.published:
            profile = getattr(self.organiser, 'organiser_profile', None)
            if not profile or not profile.is_verified:
                raise ValidationError("Organiser must be verified to publish an event.")

            # When creating, the Event has no PK yet, so we can't query related inlines.
            # Defer the beneficiary total check to the admin inline formset on create.
            if self.pk:
                total = (self.beneficiaries
                         .aggregate(models.Sum('allocation_percent'))['allocation_percent__sum'] or 0)
                if total != 100:
                    raise ValidationError("Beneficiary allocations must total exactly 100%.")
        # super().clean() not required here

    def save(self, *args, **kwargs):
        # Ensure validations run; safe because clean() now guards on self.pk
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class EventBeneficiary(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='beneficiaries')
    charity = models.ForeignKey(Charity, on_delete=models.PROTECT)
    allocation_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('event', 'charity')

    def __str__(self):
        return f"{self.charity.name} ({self.allocation_percent}%)"
