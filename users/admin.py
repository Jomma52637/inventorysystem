from django.contrib import admin
from .models import UserProfile,Technician,SubUser
# Register your models here.

admin.site.register(Technician)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'adminUser')

@admin.register(SubUser)
class SubUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'parentAccount', 'is_admin')