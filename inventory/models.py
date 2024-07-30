from django.db import models
from users.models import Technician, UserProfile

class InventoryItem(models.Model):
    barcode = models.CharField(max_length=100)
    technician = models.ForeignKey(
        Technician,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    equipment_name = models.CharField(max_length=255)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='inventory_items')
    checked_in = models.BooleanField(default=True)  # Field to indicate if item is checked in or out
    checked_out_date = models.DateField(null=True, blank=True)  # Field to store the checkout date

    class Meta:
        unique_together = ('barcode', 'user_profile')

    def __str__(self):
        return self.barcode
