from pyexpat.errors import messages
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import AdminSignUpForm,AdminLoginForm,CompanySignUpForm,SuperUserSignUpForm,UserLoginForm,UserSignUpForm,HarassmentReportForm,ErrorReportForm,CheckIdForm,SendEmailForm,SendSuperuserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users,Admin,Error_report,Text
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
    
# 管理者ホーム
class IndexView(View):
    def get(self, request):
        return render(
            request, "index.html")

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
class AdminLoginView(View):
    template_name = 'admin_login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('app:index')
        form = AdminLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            account_id = form.cleaned_data['account_id']
            password = form.cleaned_data['password']
            # password = make_password(password)  # パスワードをハッシュ化
            # user = authenticate(request, account_id=account_id, password=password)
            user = Admin.objects.filter(account_id=account_id).first()  # データベースを検索
            print('🔥')
            print(user,'ユーザー：account_id')
            print(user.password,'ユーザー：password')
            if user.check_password(password):
                login(request, user)
                return redirect('app:index')

            # if user is not None:
            #     login(request, user)
            #     return redirect('app:index')
            else:
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {"form": form})

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
class UserLoginView(View):
    template_name = 'user_login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('app:index')
        form = UserLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            account_id = form.cleaned_data['account_id']
            password = form.cleaned_data['password']
            # password = make_password(password)  # パスワードをハッシュ化
            # user = authenticate(request, account_id=account_id, password=password)
            user = Users.objects.filter(account_id=account_id).first()  # データベースを検索
            print('🔥')
            print(user,'管理者：account_id')
            print(user.password,'管理者：password') 
            if user.check_password(password):
                login(request, user)    
                return redirect('app:index')

            # if user is not None:
            #     login(request, user)
            #     return redirect('app:index')
            else:
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {"form": form})

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
        paginator = Paginator(admin_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "admin_list.html", {"page_obj": page_obj})

# 企業一覧画面
class CompanyListView(View):
    def get(self, request):
        company_list = Company.objects.all()
        paginator = Paginator(company_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "company_list.html", {"page_obj": page_obj})

# ユーザー一覧画面
class UserListView(View):
    def get(self, request):
        user_list = Users.objects.all()
        paginator = Paginator(user_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "user_list.html", {"page_obj": page_obj})

# エラー一覧画面
class ErrorReportListView(View):
    def get(self, request):
        error_list = Error_report.objects.all()
        paginator = Paginator(error_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "error_list.html", {"page_obj": page_obj})

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
class AccountInfoView(View):
    def get(self, request):
        # user = request.user  # ログインしているユーザーを取得
        # user_id = user.account_id
        # user_password_hash = user.password  # パスワードはハッシュ化されている
        return render(request, 'account_info.html')

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
            user_id = user.account_id
            if account_id == user_id:
                self.request.session['superuser_flag'] = user.superuser_flag  # セッションに保存
                return redirect("app:forget_password")
            else:
                return render(request, "check_id.html", {"form": form})
        return render(request, "check_id.html", {"form": form})

# メール送信
class ForgetPasswordView(View):
    def get(self, request):
        is_superuser = self.request.session.get('superuser_flag')

        # スーパーユーザーの場合
        if is_superuser:
            form = SendEmailForm()
            return render(request, "forget_password.html", {"form": form})
        # ユーザーの場合
        else:
            form = SendSuperuserForm()
            return render(request, "forget_password.html", {"form": form})
        
    def post(self, request):
        is_superuser = self.request.session.get('superuser_flag')

        # スーパーユーザーの場合
        if is_superuser:
            form = SendEmailForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                return redirect("app:pw_send_comp")
            return render(request, "forget_password.html", {"form": form})
        # スーパーユーザーの場合
        else:
            form = SendSuperuserForm(request.POST)
            if form.is_valid():
                return redirect("app:pw_send_comp")
            return render(request, "forget_password.html", {"form": form})
        
# メール送信完了
class PwSendCompleteView(View):
    def get(self, request):
        return render(
            request, "pw_send_comp.html")