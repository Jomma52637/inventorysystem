from django.urls import path
from .views import inventory_list, add_inventory_item, technician_list, add_technician, deactivate_technician, reactivating_technician, delete_inventory_item, check_in_out, check_in_inventory_item

urlpatterns = [
    path('inventory/', inventory_list, name='inventory_list'),
    path('add/', add_inventory_item, name='add_inventory_item'),
    path('staff/', technician_list, name='admin_dashboard'),
    path('technician/add/', add_technician, name='add_technician'),
    path('technician/deactivate/<int:technician_id>/', deactivate_technician, name='deactivate_technician'),
    path('technician/reactivate/<int:technician_id>/', reactivating_technician, name='reactivating_technician'),
    path('inventory/delete/<int:item_id>/', delete_inventory_item, name='delete_inventory_item'),
    path('inventory/check-in-out/', check_in_out, name='check_in_out'),
    path('check-in/<int:item_id>/', check_in_inventory_item, name='check_in_inventory_item'),

]
