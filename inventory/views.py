from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from .models import InventoryItem
from .forms import InventoryItemForm
from users import models as userModels
from users.forms import TechnicianForm
from django.utils import timezone
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages


@login_required
def inventory_list(request):
    # Get the user profile associated with the logged-in user
    user_profile = request.user.userprofile
    
    # Filter inventory items to include only those associated with the user's profile
    items = InventoryItem.objects.filter(user_profile=user_profile)
    
    return render(request, 'inventory/inventory_list.html', {'items': items})

@login_required
def check_in_inventory_item(request, item_id):
    print("Received request to check in item:", item_id)  # Debugging line
    if request.method == 'POST':
        barcode = request.POST.get('barcode', '').strip()
        item = get_object_or_404(InventoryItem, id=item_id)
        
        print("Received barcode:", barcode)  # Debugging line

        if item.barcode == barcode:
            if not item.checked_in:
                item.checked_in = True
                item.checked_out_date = None
                item.technician = None
                item.save()
                messages.success(request, "Item checked in successfully!")
                print("Item checked in successfully!")  # Debugging line
            else:
                messages.info(request, "Item is already checked in.")
                print("Item is already checked in.")  # Debugging line
        else:
            messages.error(request, "Barcode does not match the item.")
            print("Barcode does not match the item.")  # Debugging line

    return redirect('inventory_list')


@login_required
def add_inventory_item(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.user_profile = request.user.userprofile  # Set user profile
                item.save()
                messages.success(request, "Item added successfully!")
                return redirect('inventory_list')  # Redirect to inventory list or appropriate page
            except IntegrityError:
                form.add_error(None, "An item with this barcode already exists.")
    else:
        form = InventoryItemForm()

    return render(request, 'inventory/add_inventory_item.html', {'form': form})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CheckInOutForm
from .models import InventoryItem, Technician, UserProfile

@login_required
def check_in_out(request):
    technicians = Technician.objects.filter(user_profile=request.user.userprofile)  # Adjust as needed

    if request.method == 'POST':
        form = CheckInOutForm(request.POST, technicians=technicians)
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            technician = form.cleaned_data['technician_name']
            
            # Validate that the technician field is not empty
            if not technician:
                messages.error(request, "Technician field is required.")
                return redirect('check_in_out')

            try:
                item = InventoryItem.objects.get(barcode=barcode, user_profile=request.user.userprofile)
            except InventoryItem.DoesNotExist:
                messages.error(request, "This item isn't marked in inventory.")
                return redirect('check_in_out')

            # Check if the item is currently checked in or checked out
            if item.checked_in:
                # Item is checked in, so we need to check it out
                item.checked_in = False
                item.technician = technician
                item.checked_out_date = timezone.now()  # Set the checked out date
                messages.success(request, "Item checked out successfully!")
            else:
                # Item is checked out, so we need to check it in
                item.checked_in = True
                item.technician = None
                item.checked_out_date = None  # Clear the checked out date
                messages.success(request, "Item checked in successfully!")

            item.save()
            return redirect('check_in_out')  # Redirect to the same view or another view
        else:
            messages.error(request, "Form is not valid.")
    else:
        form = CheckInOutForm(technicians=technicians)

    return render(request, 'inventory/check_in_out.html', {'form': form})



@login_required
def delete_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_list')  # Redirect to the inventory list after deletion
    
    return render(request, 'inventory/confirm_delete.html', {'item': item})




@login_required
def technician_list(request):
    try:
        user_profile = userModels.UserProfile.objects.get(user=request.user)
    except userModels.UserProfile.DoesNotExist:
        return redirect('error_page')  # Handle the case where the user profile does not exist

    filter_status = request.GET.get('status', 'active')  # Default to 'active'
    
    if filter_status == 'active':
        technicians = userModels.Technician.objects.filter(user_profile=user_profile, active=True)
    elif filter_status == 'inactive':
        technicians = userModels.Technician.objects.filter(user_profile=user_profile, active=False)
    else:
        technicians = userModels.Technician.objects.filter(user_profile=user_profile)
    
    context = {
        'technicians': technicians,
        'filter_status': filter_status
    }
    return render(request, 'admin/technician_list.html', context)



def deactivate_technician(request, technician_id):
    technician = get_object_or_404(userModels.Technician, id=technician_id)
    technician.active = False
    technician.save()
    # Preserve the filter status
    status = request.GET.get('status', 'active')
    return redirect(f"{reverse('admin_dashboard')}?status={status}")

def reactivating_technician(request, technician_id):
    technician = get_object_or_404(userModels.Technician, id=technician_id)
    technician.active = True
    technician.save()
    # Preserve the filter status
    status = request.GET.get('status', 'inactive')
    return redirect(f"{reverse('admin_dashboard')}?status={status}")

@login_required
def add_technician(request):
    if request.method == 'POST':
        form = TechnicianForm(request.POST)
        if form.is_valid():
            tech_name = form.cleaned_data['tech_name']
            # Create a Technician and link it to the current user's profile
            userModels.Technician.objects.create(
                tech_name=tech_name,
                user_profile=request.user.userprofile  # Assuming userprofile is related to the User model
            )
            return redirect('admin_dashboard')  # Redirect to the technician list or another appropriate page
    else:
        form = TechnicianForm()

    return render(request, 'admin/add_technician.html', {'form': form})