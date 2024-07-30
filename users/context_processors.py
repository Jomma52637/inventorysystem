# users/context_processors.py

from .models import UserProfile

def is_admin(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return {'is_admin': user_profile.adminUser}
        except UserProfile.DoesNotExist:
            return {'is_admin': False}
    return {'is_admin': False}
