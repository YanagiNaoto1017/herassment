from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Admin,Company


class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ("account_id","email",)

class AdminLoginFrom(AuthenticationForm):
    class Meta:
        model = Admin


class CompanySignUpForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("id","company_name",)
        labels = {'id':'企業ID', 'company_name':'企業名'}