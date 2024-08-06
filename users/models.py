from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adminUser = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class SubUser(models.Model):
    parentAccount = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sub_users')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Technician(models.Model):
    tech_name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='technicians')

    def __str__(self):
        return self.tech_name