from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    # You can customize the form here if needed
    pass

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True, help_text="Enter your phone number")

    class Meta:
        model = User
        fields = ("username","first_name", "phone", "last_name","email", "password1", "password2", )
        

