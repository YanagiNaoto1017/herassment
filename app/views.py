from pyexpat.errors import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import AdminSignUpForm,AdminLoginForm,CompanySignUpForm,SuperUserSignUpForm,UserLoginForm,UserSignUpForm,HarassmentReportForm,ErrorReportForm,CheckIdForm,SendEmailForm,SendSuperuserForm,DetectionForm,CustomPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users,Error_report,Text,Harassment_report,Dictionary,Notification
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator

# ホーム
class IndexView(LoginRequiredMixin,View):
    def get(self, request):
        return render(
            request, "index.html")

# 管理者新規登録
class SignupView(LoginRequiredMixin,CreateView):
    form_class = AdminSignUpForm
    template_name = "admin_signup.html"
    success_url = reverse_lazy("app:complete")

    def form_valid(self, form):
        user = form.save(commit=False)  # フォームの save を呼び出す
        user.admin_flag = True # 管理者フラグをTrue
        user.start_password = user.password # 初期パスワードにも登録
        user.save()
        return super().form_valid(form)
    
# 管理者ログイン
class AdminLoginView(BaseLoginView):
    form_class = AdminLoginForm
    template_name = 'admin_login.html'

# ログアウト
class LogoutView(BaseLogoutView):

    def get(self, request):
        logout(request)
        return redirect('user_login')
    
# 企業登録
class CompanySignupView(LoginRequiredMixin,CreateView):
    form_class = CompanySignUpForm
    template_name = "company_signup.html"
    success_url = reverse_lazy("app:complete")

# スーパーユーザー登録
class SuperUserSignupView(LoginRequiredMixin,CreateView):
    form_class = SuperUserSignUpForm
    template_name = "superuser_signup.html"
    success_url = reverse_lazy("app:complete")

    def form_valid(self, form):
        user = form.save(commit=False)  # フォームの save を呼び出す
        user.superuser_flag = True # スーパーユーザーフラグをTrue
        user.user_flag = True # ユーザーフラグをTrue
        user.start_password = user.password # 初期パスワードにも登録
        user.save()
        return super().form_valid(form)

# ユーザーログイン
class UserLoginView(BaseLoginView):
    form_class = UserLoginForm
    template_name = 'user_login.html'

# 登録完了画面
class CompleteView(LoginRequiredMixin,View):
    def get(self, request):

        return render(
            request, "complete.html")

# 報告完了画面
class ReportCompleteView(LoginRequiredMixin,View):
    def get(self, request):

        return render(
            request, "report_complete.html")

# 削除完了画面
class DeleteCompleteView(LoginRequiredMixin,View):
    def get(self, request):

        return render(
            request, "delete_complete.html")

# 管理者一覧画面
class AdminListView(LoginRequiredMixin,View):
    def get(self, request):
        user = Users.objects.filter(admin_flag=True)  # データベースを検索
        paginator = Paginator(user, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "admin_list.html", {"page_obj": page_obj})

# 企業一覧画面
class CompanyListView(LoginRequiredMixin,View):
    def get(self, request):
        company_list = Company.objects.all()
        paginator = Paginator(company_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "company_list.html", {"page_obj": page_obj})

# ユーザー一覧画面
class UserListView(LoginRequiredMixin,View):
    def get(self, request):
        # スーパーユーザーの場合
        if request.user.superuser_flag:
            company = request.user.company
            user = Users.objects.filter(user_flag=True,company=company)  # データベースを検索
        # 管理者の場合
        elif request.user.admin_flag:
            user = Users.objects.filter(user_flag=True)  # データベースを検索
        paginator = Paginator(user, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "user_list.html", {"page_obj": page_obj})

# エラー一覧画面
class ErrorReportListView(LoginRequiredMixin,View):
    def get(self, request):
        error_list = Error_report.objects.all()
        paginator = Paginator(error_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "error_list.html", {"page_obj": page_obj})

# 検出画面
class DetectionView(View):
    def get(self, request):
        form = DetectionForm()
        return render(request, 'detection.html', {'form': form})

    def post(self, request):
        form = DetectionForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']
            detected_words = []
            # 辞書からキーワードを取得
            keywords = Dictionary.objects.values_list('keyword', flat=True)

            # 入力テキストにキーワードが含まれているかチェック
            for keyword in keywords:
                if keyword in input_text:
                    detected_words.append(keyword)

            # ハラスメントフラグの設定
            harassment_flag = len(detected_words) > 0

            # テキストを保存
            text_instance = Text.objects.create(
                input_text=input_text,
                harassment_flag=harassment_flag,
                detected_words=', '.join(detected_words) if detected_words else None
            )

            return render(request, 'detection_result.html', {
                'input_text': input_text,
                'detected_words': detected_words,
                'harassment_flag': harassment_flag,
                'id': id
            })
        return render(request, 'detection.html', {'form': form})

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
class UserSignupView(LoginRequiredMixin,CreateView):
    form_class = UserSignUpForm
    template_name = "user_signup.html"
    success_url = reverse_lazy("app:complete")

    def form_valid(self, form):
        user = form.save(commit=False)  # フォームの save を呼び出す
        user.user_flag = True # ユーザーフラグをTrue
        user.company = self.request.user.company # ログインしているスーパーユーザーの企業IDをユーザーにも登録
        user.start_password = user.password # 初期パスワードにも登録
        user.save()
        return super().form_valid(form)

# エラー報告画面
class ErrorReportView(LoginRequiredMixin,View):
    def get(self, request):
        form = ErrorReportForm()
        return render(request, "error_report.html", {"form": form})
    
    def post(self, request):
        form = ErrorReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:report_complete")
        return render(request, "error_report.html", {"form": form})

# ハラスメント報告画面
class HarassmentReportView(LoginRequiredMixin,View):
    def get(self, request):
        form = HarassmentReportForm()
        return render(request, "harassment_report.html", {"form": form})
    
    def post(self, request):
        form = HarassmentReportForm(request.POST)
        if form.is_valid():
            harassment_report = form.save(commit=False)  # フォームの save を呼び出す
            harassment_report.company_id = request.user.company.id # ログインユーザーの企業IDを登録
            form.save()
            return redirect("app:report_complete")
        return render(request, "harassment_report.html", {"form": form})
    
# ハラスメント一覧画面
class HarassmentReportListView(LoginRequiredMixin,View):
    def get(self, request):
        harassment_list = Harassment_report.objects.filter(company_id=request.user.company.id)
        paginator = Paginator(harassment_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "harassment_list.html", {"page_obj": page_obj})

# アカウント情報確認画面
class AccountInfoView(LoginRequiredMixin,View):
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
            user_id = user.account_id
            if account_id == user_id:
                self.request.session['account_id'] = user.account_id  # セッションに保存
                self.request.session['company_id'] = user.company.id  # セッションに保存
                self.request.session['superuser_flag'] = user.superuser_flag  # セッションに保存
                self.request.session['user_flag'] = user.user_flag  # セッションに保存
                return redirect("app:forget_password")
            else:
                return render(request, "check_id.html", {"form": form})
        return render(request, "check_id.html", {"form": form})

# メール送信
class ForgetPasswordView(View):
    def get(self, request):
        superuser_flag = self.request.session.get('superuser_flag')
        user_flag = self.request.session.get('user_flag')
        company_id = self.request.session.get('company_id')
        # スーパーユーザーの場合
        if superuser_flag and user_flag:
            form = SendEmailForm()
        # ユーザーの場合
        elif not superuser_flag and user_flag:
            form = SendSuperuserForm()
        return render(request, "forget_password.html", {"form": form})
        
    def post(self, request):
        superuser_flag = self.request.session.get('superuser_flag')
        user_flag = self.request.session.get('user_flag')
        account_id = self.request.session.get('account_id')
        
        # スーパーユーザーの場合
        if superuser_flag and user_flag:
            form = SendEmailForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                return redirect("app:pw_send_comp")
            return render(request, "forget_password.html", {"form": form})
        # ユーザーの場合
        elif not superuser_flag and user_flag:
            form = SendSuperuserForm(request.POST)
            if form.is_valid():
                superuser_id = form.cleaned_data['superuser_name']
                user = Users.objects.filter(account_id=account_id).first()  # データベースを検索
                notification = Notification.objects.create(
                    account_name = user.account_name,
                    company_id = user.company.id,
                    superuser_id = superuser_id,
                )
                notification.save()
                return redirect("app:pw_send_comp")
            return render(request, "forget_password.html", {"form": form})
        
# メール送信完了
class PwSendCompleteView(View):
    def get(self, request):
        return render(
            request, "pw_send_comp.html")
    
#パスワード変更画面
class PasswordChangeView(LoginRequiredMixin,View):
    template_name = 'password_change.html'  # パスワード変更用のテンプレート
    form_class = CustomPasswordChangeForm
    
    def get(self, request):
        form = CustomPasswordChangeForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomPasswordChangeForm(request.POST)
        user = Users.objects.get(id=request.user.id)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            new_password = make_password(new_password)            
            user.password = new_password
            user.save()
            update_session_auth_hash(request, user)
        return render(request, "pw_complete.html", {"form": form})    

class PwChangeCompleteView(View):
    template_name = 'pw_complete.html'  # パスワード変更完了用のテンプレート

# PWリセット通知
class NotificationView(View):
    template_name = 'notification.html'
    def get(self, request):
        notification = Notification.objects.filter(company_id=request.user.company.id, superuser_id=request.user.account_id, is_read=False)  # データベースを検索
        paginator = Paginator(notification, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, "notification.html", {"page_obj": page_obj})
    
# ユーザー削除
class UserDeleteView(DeleteView):
    model = Users
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('app:user_list')

# 管理者削除
class AdminDeleteView(DeleteView):
    model = Users
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('app:admin_list')

# 企業削除
class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'company_confirm_delete.html'
    success_url = reverse_lazy('app:company_list')

# パスワードリセット
class PasswordReset(LoginRequiredMixin, View):
    template_name = 'confirm_pw_reset.html'
    
    def get(self, request, account_name):
        user = Users.objects.get(account_name=account_name)
        return render(request, self.template_name, {"object": user})
    
    def post(self, request, account_name):
        if request.method == 'POST':
            user = Users.objects.get(account_name=account_name)
            notification = Notification.objects.get(account_name=account_name)
            user.password = user.start_password # 初期パスワードを代入
            notification.is_read = True # リセットした通知をTrueに変更
            user.save()
            notification.save()
            return redirect('app:notification')
        return render(request, self.template_name)

# エラー
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_403_view(request, exception):
    return render(request, '403.html', status=403)

def custom_500_view(request):
    return render(request, '500.html', status=500)