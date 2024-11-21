from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import AdminSignUpForm,AdminLoginForm,CompanySignUpForm,SuperUserSignUpForm,UserLoginForm,UserSignUpForm,HarassmentReportForm,ErrorReportForm,CheckIdForm,SendEmailForm,SendSuperuserForm,TextForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users,Admin,Error_report,Text,Dictionary
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
    form_class = TextForm
    success_url = reverse_lazy('detection')

    def form_valid(self, form):
        input_text = form.cleaned_data['input_text']
        detected_words = self.detect_harassment(input_text)
        harassment_flag = bool(detected_words)

        # モデルのインスタンスを作成
        text_instance = form.save(commit=False)
        text_instance.harassment_flag = harassment_flag
        text_instance.detected_words = ', '.join(detected_words)
        text_instance.save()

        return super().form_valid(form)

    def detect_harassment(self, text):
        # 辞書からキーワードを取得
        keywords = Dictionary.objects.values_list('keyword', flat=True)
        detected_words = [word for word in keywords if word in text]
        return detected_words
    

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

# アカウント情報確認画面
class AccountInfoView(View):
    def get(self, request):
        print(request.user)
        user = request.user  # ログインしているユーザーを取得
        user_info = Users.objects.filter(account_id=user.id)  # Usersモデルからログインユーザーの情報を取得
        print(user_info)
        return render(request, 'account_info.html', {
            'object_list': user_info,  # テンプレートに渡す変数
        })

# ID確認
class CheckIdView(View):
    def get(self, request):
        form = CheckIdForm()
        return render(request, "check_id.html", {"form": form})
    
    def post(self, request):
        form = CheckIdForm(request.POST)
        if form.is_valid():
            account_id = form.cleaned_data['account_id']
            user = Users.objects.filter(account_id=account_id).first()  # データベースを検索
            if user:
                superuser_flag = user.superuser_flag  # superuser_flagを取得
                self.request.session['superuser_flag'] = superuser_flag  # セッションに保存
            return redirect("app:forget_password")
        return render(request, "check_id.html", {"form": form})

# メール送信
class ForgetPasswordView(View):
    def get(self, request):
        is_superuser = request.session.get('superuser_flag')

        if is_superuser == True:
            form = SendEmailForm()
            return render(request, "forget_password.html", {"form": form})
        else:
            form = SendSuperuserForm()
            return render(request, "forget_password.html", {"form": form})
        
    def post(self, request):
        is_superuser = request.session.get('superuser_flag')

        if is_superuser == True:
            form = SendEmailForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                return redirect("app:pw_send_comp")
            return render(request, "forget_password.html", {"form": form})
        else:
            form = SendSuperuserForm(request.POST)
            if form.is_valid():
                return redirect("app:pw_send")
            return render(request, "forget_password.html", {"form": form})
        
# メール送信完了
class PwSendCompleteView(View):
    def get(self, request):
        return render(
            request, "pw_send_comp.html")
    
#パスワード変更画面
class PasswordChangeView(View):
    template_name = 'password_change.html'  # パスワード変更用のテンプレート
    success_url = reverse_lazy('app:pw_change_complete')  # 成功後のリダイレクト先

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class PwChangeCompleteView(View):
    template_name = 'pw_change_complete.html'  # パスワード変更完了用のテンプレート