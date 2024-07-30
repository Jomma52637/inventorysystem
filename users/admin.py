from django.contrib import admin
from .models import UserProfile,Technician
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Technician)