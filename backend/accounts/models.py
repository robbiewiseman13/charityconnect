from django.conf import settings
from django.db import models

class OrganiserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organiser_profile'
    )
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Organiser<{self.user.get_username()}>"
