from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import AdminSignUpForm,AdminLoginForm,CompanySignUpForm,SuperUserSignUpForm,UserLoginForm,UserSignUpForm,HarassmentReportForm,ErrorReportForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users,Admin,Error_report,Text,Harassment_report
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
    
# ホーム
class IndexView(TemplateView):

    template_name = 'index.html'

# ホーム
class UserIndexView(TemplateView):

    template_name = 'user_index.html'

# 管理者新規登録
class SignupView(LoginRequiredMixin,CreateView):

    form_class = AdminSignUpForm
    template_name = 'admin_signup.html'
    success_url = reverse_lazy("app:complete")
    
# 管理者ログイン
class LoginView(BaseLoginView):

    form_class = AdminLoginForm
    template_name = "admin_login.html"

    def post(self, request, *args, **kwargs):
        # 通常のログイン処理を実行
        return redirect('app:index')

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

    def post(self, request, *args, **kwargs):

        print(self.request)
        # 通常のログイン処理を実行
        return redirect('app:user_index')

# 登録完了画面
class CompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'complete.html'

# 報告完了画面
class ReportCompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'report_complete.html'

# 削除完了画面
class DeleteCompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'delete_complete.html'

# 管理者一覧画面
class AdminListView(LoginRequiredMixin,ListView):
    model = Admin
    template_name = 'admin_list.html'

# 企業一覧画面
class CompanyListView(LoginRequiredMixin,ListView):
    model = Company
    template_name = 'company_list.html'

# ユーザー一覧画面
class UserListView(LoginRequiredMixin,ListView):
    model = Users
    template_name = 'user_list.html'

# エラー一覧画面
class ErrorReportListView(LoginRequiredMixin,ListView):
    model = Error_report
    template_name = 'error_list.html'

# 検出画面
class DetectionView(LoginRequiredMixin, CreateView):
    model = Text
    template_name = 'detection.html'
    fields = ['input_text', 'harassment_flag', 'text_flag', 'detected_words']

# 校正画面
class ProofreadingView(LoginRequiredMixin,CreateView):
    model = Text
    template_name = 'proofreading.html'
    fields = ['input_text', 'harassment_flag', 'text_flag', 'detected_words']

# ユーザー登録
class UserSignupView(LoginRequiredMixin,CreateView):

    model = Users
    form_class = UserSignUpForm
    template_name = 'user_signup.html'
    success_url = reverse_lazy("app:complete")

# エラー報告画面
class ErrorReportView(LoginRequiredMixin,CreateView):

    model = Error_report
    form_class = ErrorReportForm
    template_name = 'error_report.html'
    success_url = reverse_lazy("app:report_complete")

# ハラスメント報告画面
class HarassmentReportView(LoginRequiredMixin,CreateView):

    model = Harassment_report
    form_class = HarassmentReportForm
    template_name = 'harassment_report.html'
    success_url = reverse_lazy("app:report_complete")
