from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, SubUser

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check if a UserProfile should be created
        if hasattr(instance, 'profile'):  # Ensure we have the right check here
            UserProfile.objects.create(user=instance)
