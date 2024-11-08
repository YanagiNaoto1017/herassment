from django.shortcuts import render
from django.contrib.auth import login, authenticate

from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from .forms import SignUpForm
# from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Admin

class IndexView(TemplateView):

    template_name = 'index.html'

class LoginView(TemplateView):

    template_name = 'admin_login.html'

class SignupView(TemplateView):
    """管理者登録用ビュー"""

    form_class = SignUpForm
    template_name = 'admin_signup.html'
    success_url = reverse_lazy("app:index")

    def form_valid(self, form):
        # ユーザー作成後にそのままログイン状態にする設定
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return response