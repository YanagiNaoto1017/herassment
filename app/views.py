from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import AdminSignUpForm,AdminLoginForm,CompanySignUpForm,SuperUserSignUpForm,UserLoginForm,UserSignUpForm,HarassmentReportForm,ErrorReportForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users,Admin,Error_report,Text
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
    
# 管理者ホーム
class IndexView(View):
    def get(self, request):
        # ログイン中のユーザー情報を利用
        is_superuser = request.user.is_authenticated and getattr(request.user, 'superuser_flag', True)
        is_staff = request.user.is_authenticated and getattr(request.user, 'is_staff', True)
        
        return render(
            request, 
            "index.html", 
            {"is_superuser": is_superuser, "is_staff": is_staff}
        )

# 管理者新規登録
class SignupView(View):
    def get(self, request):
        form = AdminSignUpForm()
        return render(request, "admin_signup.html", {"form": form})
    
    def post(self, request):
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:conmplete")
        return render(request, "admin_signup.html", {"form": form})
    
# 管理者ログイン
class AdminLoginView(BaseLoginView):

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
class CompanySignupView(View):
    def get(self, request):
        form = CompanySignUpForm()
        return render(request, "company_signup.html", {"form": form})
    
    def post(self, request):
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:conmplete")
        return render(request, "company_signup.html", {"form": form})

# スーパーユーザー登録
class SuperUserSignupView(View):
    def get(self, request):
        form = SuperUserSignUpForm()
        return render(request, "superuser_signup.html", {"form": form})
    
    def post(self, request):
        form = SuperUserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:conmplete")
        return render(request, "superuser_signup.html", {"form": form})

# ユーザーログイン
class UserLoginView(BaseLoginView):
    form_class = UserLoginForm
    template_name = 'user_login.html'

    def post(self, request, *args, **kwargs):

        print(self.request)
        # 通常のログイン処理を実行
        return redirect('app:index')

# 登録完了画面
class CompleteView(View):
    def get(self, request):

        return render(
            request, "complete.html")

# 報告完了画面
class ReportCompleteView(View):
    def get(self, request):

        return render(
            request, "report_complete.html")

# 削除完了画面
class DeleteCompleteView(View):
    def get(self, request):

        return render(
            request, "delete_complete.html")

# 管理者一覧画面
class AdminListView(View):
    def get(self, request):
        admin_list = Admin.objects.all()
        return render(request, "admin_list.html", {"admin_list": admin_list})

# 企業一覧画面
class CompanyListView(View):
    def get(self, request):
        company_list = Company.objects.all()
        return render(request, "company_list.html", {"company_list": company_list})

# ユーザー一覧画面
class UserListView(View):
    def get(self, request):
        user_list = Users.objects.all()
        return render(request, "user_list.html", {"user_list": user_list})

# エラー一覧画面
class ErrorReportListView(View):
    def get(self, request):
        error_list = Error_report.objects.all()
        return render(request, "error_list.html", {"error_list": error_list})

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
class UserSignupView(View):
    def get(self, request):
        form = UserSignUpForm()
        return render(request, "user_signup.html", {"form": form})
    
    def post(self, request):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:conmplete")
        return render(request, "user_signup.html", {"form": form})

# エラー報告画面
class ErrorReportView(View):
    def get(self, request):
        form = ErrorReportForm()
        return render(request, "error_report.html", {"form": form})
    
    def post(self, request):
        form = ErrorReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:report_conmplete")
        return render(request, "error_report.html", {"form": form})

# ハラスメント報告画面
class HarassmentReportView(View):
    def get(self, request):
        form = HarassmentReportForm()
        return render(request, "harassment_report.html", {"form": form})
    
    def post(self, request):
        form = HarassmentReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:report_conmplete")
        return render(request, "harassment_report.html", {"form": form})


#アカウント情報確認画面
def account_info(request):
    user = request.user  # ログインしているユーザーを取得
    user_id = user.id
    user_password_hash = user.password  # パスワードはハッシュ化されている

    return render(request, 'account_info.html', {
        'user_id': user_id,
        'user_password_hash': user_password_hash,
    })