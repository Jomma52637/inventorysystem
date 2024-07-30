from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from . import forms


def register(request):
    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}, your account is created, please login.")
            return redirect('user-login')
    else:
        form = forms.UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# @login_required
# def profile(request):
#     user = request.user
    
#     return render(request, 'users/profile.html', {'tasks': tasks, 'user': user})

@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'users/logout.html', {})
    else:
        return render(request, 'users/logout_already.html')

