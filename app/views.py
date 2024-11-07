from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView as AuthLogoutView  # インポートを追加
from .forms import SignUpForm
from .forms import LoginForm

class IndexView(TemplateView):
    template_name = 'index.html'

class LoginView(TemplateView):
    form_class = LoginForm  # 修正
    template_name = 'admin_login.html'

class SignupView(TemplateView):
    """管理者登録用ビュー"""
    form_class = SignUpForm
    template_name = 'admin_signup.html'
    success_url = reverse_lazy("app:index")

class LogoutView(AuthLogoutView):  # 修正
    template_name = 'admin_logout.html'
    success_url = reverse_lazy("accounts:index")