from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import AdminSignUpForm,AdminLoginForm,CompanySignUpForm,SuperUserSignUpForm,UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render

# ホーム
class IndexView(TemplateView,LoginRequiredMixin):

    template_name = 'index.html'

# 管理者新規登録
class SignupView(LoginRequiredMixin,CreateView):

    form_class = AdminSignUpForm
    template_name = 'admin_signup.html'
    success_url = reverse_lazy("app:complete")
    
# 管理者ログイン
class LoginView(BaseLoginView):

    form_class = AdminLoginForm
    template_name = "admin_login.html"

# ログアウト
class LogoutView(BaseLogoutView):

    def get(self, request):
        logout(request)
        return redirect('user_login')
    
# 企業登録
class CompanySignupView(LoginRequiredMixin,CreateView):

    model = Company
    form_class = CompanySignUpForm
    template_name = 'company_signup.html'
    success_url = reverse_lazy("app:complete")

# スーパーユーザー登録
class SuperUserSignupView(LoginRequiredMixin,CreateView):

    model = Users
    form_class = SuperUserSignUpForm
    template_name = 'superuser_signup.html'
    success_url = reverse_lazy("app:complete")

# ユーザーログイン
class UserLoginView(BaseLoginView):
    form_class = UserLoginForm
    template_name = 'user_login.html'

# 完了画面
class CompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'complete.html'