from django.shortcuts import render

from django.views.generic.base import TemplateView, ListView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
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

class ListView(LoginRequiredMixin, ListView):
    """管理者一覧"""

    model = Admin
    form_class = AdminListForm
    template_name = 'admin_list.html'