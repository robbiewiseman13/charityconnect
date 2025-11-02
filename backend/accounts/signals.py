from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrganiserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_organiser_profile(sender, instance, created, **kwargs):
    # Create on first save, ensure it exists later
    if created:
        OrganiserProfile.objects.create(user=instance)
    else:
        OrganiserProfile.objects.get_or_create(user=instance)
