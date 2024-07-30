from django.urls import path
from .views import register, create_user_profile, create_technician, user_logout

urlpatterns = [
    path('register/', register, name='register'),
    path('create-user-profile/', create_user_profile, name='create_user_profile'),
    path('create-technician/', create_technician, name='create_technician'),
    path('logout/', user_logout, name='user_logout'),
]
