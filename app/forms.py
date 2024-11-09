from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Admin


class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = (
            "account_id",
            "email",
        )

class AdminLoginFrom(AuthenticationForm):
    class Meta:
        model = Admin