from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Admin


class SignUpForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = (
            "email",
            "password",
        )

class LoginForm(AuthenticationForm):
    class Meta:
        model = Admin