from django.contrib import admin
from django.urls import include
from django.urls import path
from inventory import views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inventory_list, name='inventory_list'),
    path('', include('inventory.urls')),
    path('add/', views.add_inventory_item, name='add_inventory_item'),
    path("register/", user_views.register, name='user-register'),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name='user-login'),
    path('logout/', user_views.user_logout, name="user-logout"),
]
