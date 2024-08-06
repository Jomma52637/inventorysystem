from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Technician, SubUser


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SubUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = SubUser
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=User.objects.make_random_password()  # Assign a random password
        )
        sub_user = super().save(commit=False)
        sub_user.user = user
        if commit:
            sub_user.save()
        return sub_user

class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['tech_name', 'active']
