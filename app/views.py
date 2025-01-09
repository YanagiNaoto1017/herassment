
from pyexpat.errors import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import AdminSignUpForm,CompanySignUpForm,SuperUserSignUpForm,LoginForm,UserSignUpForm,HarassmentReportForm,ErrorReportForm,CheckIdForm,SendEmailForm,SendSuperuserForm,DetectionForm,CustomPasswordChangeForm,SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users,Error_report,Text,Harassment_report,Dictionary,Notification
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q

import spacy
from django.core.mail import send_mail
from django.conf import settings
 
# メール送信関数
def send_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # 送信者のメールアドレス
        [to_email],  # 受信者のメールアドレス
        fail_silently=False,
    )

# ホーム画面表示
class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "index.html"

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

# ログアウト
class LogoutView(BaseLogoutView):
    success_url = reverse_lazy("app:login")
    
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

# ログイン
class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = 'login.html'

# 登録完了画面
class CompleteView(LoginRequiredMixin,TemplateView):
    template_name = "complete.html"

# 報告完了画面
class ReportCompleteView(LoginRequiredMixin,TemplateView):
    template_name = "report_complete.html"

# 削除完了画面
class DeleteCompleteView(LoginRequiredMixin,TemplateView):
    template_name = "delete_complete.html"

# 管理者一覧画面
class AdminListView(LoginRequiredMixin,TemplateView):
    template_name = "admin_list.html"
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        user = Users.objects.filter(admin_flag=True)  # 管理者を取得
        paginator = Paginator(user, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text'] # 入力されたテキスト
            user = Users.objects.filter(admin_flag=True,account_id__icontains=search_text)  # 条件に一致するユーザーを取得
            paginator = Paginator(user, 10) # 1ページ当たり10件
            page_number = request.GET.get('page') # 現在のページ番号を取得
            page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})

# 企業一覧画面
class CompanyListView(LoginRequiredMixin,TemplateView):
    template_name = "company_list.html"
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        company_list = Company.objects.all() # 企業を取得
        paginator = Paginator(company_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj,"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text'] # 入力されたテキスト
            company_list = Company.objects.filter(company_name__icontains=search_text) # 条件に一致する企業を取得
            paginator = Paginator(company_list, 10) # 1ページ当たり10件
            page_number = request.GET.get('page') # 現在のページ番号を取得
            page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj,"form": form})

# ユーザー一覧画面
class UserListView(LoginRequiredMixin,TemplateView):
    template_name = "user_list.html"
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        # スーパーユーザーの場合
        if request.user.superuser_flag:
            user = Users.objects.filter(user_flag=True,company=request.user.company)  # 条件に一致するユーザーを取得
        # 管理者の場合
        elif request.user.admin_flag:
            user = Users.objects.filter(user_flag=True)  # ユーザーを取得
        paginator = Paginator(user, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text'] # 入力されたテキスト
            # スーパーユーザーの場合
            if request.user.superuser_flag:
                user = Users.objects.filter(user_flag=True,company=request.user.company).filter(Q(account_name__icontains=search_text)) # 条件に一致するユーザーを取得
            # 管理者の場合
            elif request.user.admin_flag:
                user = Users.objects.filter(user_flag=True).filter(Q(account_id__icontains=search_text) | Q(account_name__icontains=search_text))  # 条件に一致する管理者を取得
            paginator = Paginator(user, 10) # 1ページ当たり10件
            page_number = request.GET.get('page') # 現在のページ番号を取得
            page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})


# エラー一覧画面
class ErrorReportListView(LoginRequiredMixin,TemplateView):
    template_name = "error_list.html"
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        error_list = Error_report.objects.all() # エラー報告を取得
        paginator = Paginator(error_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['search_text'] # 入力されたテキスト
            error_list = Error_report.objects.filter(error_detail__icontains=search_text) # 条件に一致するエラー報告を取得
            paginator = Paginator(error_list, 10) # 1ページ当たり10件
            page_number = request.GET.get('page') # 現在のページ番号を取得
            page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})

# 検出画面
class DetectionView(LoginRequiredMixin,TemplateView):
    template_name = 'detection.html'
    form_class = DetectionForm
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        nlp = spacy.load("ja_core_news_sm") # モデルのロード
        form = self.form_class(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text'] # 入力されたテキスト
            
            doc = nlp(input_text) # テキストを解析

            keywords = Dictionary.objects.values_list('keyword', flat=True) # 辞書からキーワードを取得

            detected_words = [token.text for token in doc if token.text in keywords] # 辞書との照合

            # 検出単語がある場合
            if detected_words:
                print('検出あり')

                text_instance = Text.objects.create(
                    input_text=input_text, # 入力されたテキストを保存
                    harassment_flag=True, # ハラスメントフラグをTrue
                    detected_words=', '.join(detected_words) if detected_words else None
                )
                return render(request, self.template_name, {'form': form, 'text': text_instance})
            
            # 検出単語がない場合
            else:
                print('検出なし')

                text_instance = Text.objects.create(
                    input_text=input_text, # 入力されたテキストを保存
                    harassment_flag=False, # ハラスメントフラグをFalse
                )
                return render(request, self.template_name, {'form': form, 'text': text_instance})
        return render(request, self.template_name, {'form': form})
    

# 校正画面
class ProofreadingView(LoginRequiredMixin,TemplateView):
    template_name = 'detection.html'
    form_class = DetectionForm
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        nlp = spacy.load("ja_core_news_sm") # モデルのロード
        form = self.form_class(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text'] # 入力されたテキスト
            
            doc = nlp(input_text) # テキストを解析

            keywords = Dictionary.objects.values_list('keyword', flat=True) # 辞書からキーワードを取得

            detected_words = [token.text for token in doc if token.text in keywords] # 辞書との照合

            # 検出単語がある場合
            if detected_words:
                print('検出あり')

                text_instance = Text.objects.create(
                    input_text=input_text, # 入力されたテキストを保存
                    harassment_flag=True, # ハラスメントフラグをTrue
                    detected_words=', '.join(detected_words) if detected_words else None
                )
                return render(request, self.template_name, {'form': form, 'text': text_instance})
            
            # 検出単語がない場合
            else:
                print('検出なし')

                text_instance = Text.objects.create(
                    input_text=input_text, # 入力されたテキストを保存
                    harassment_flag=False, # ハラスメントフラグをFalse
                )
                return render(request, self.template_name, {'form': form, 'text': text_instance})
        return render(request, self.template_name, {'form': form})

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
class ErrorReportView(LoginRequiredMixin,TemplateView):
    template_name = "error_report.html"
    form_class = ErrorReportForm
    success_url = reverse_lazy("app:report_complete")

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save() # 入力内容を保存
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})

# ハラスメント報告画面
class HarassmentReportView(LoginRequiredMixin,TemplateView):
    template_name = "harassment_report.html"
    form_class = HarassmentReportForm
    success_url = reverse_lazy("app:report_complete")

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            harassment_report = form.save(commit=False)  # フォームの save を呼び出す
            harassment_report.company_id = request.user.company.id # ログインユーザーの企業IDを登録
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})
    
# ハラスメント一覧画面
class HarassmentReportListView(LoginRequiredMixin,TemplateView):
    template_name = "harassment_list.html"

    def get(self, request):
        harassment_list = Harassment_report.objects.filter(company_id=request.user.company.id) # 同じ企業IDのハラスメント報告を取得
        paginator = Paginator(harassment_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj})
    
# ハラスメント詳細画面
class HarassmentDetailView(LoginRequiredMixin, TemplateView):
    template_name = "harassment_detail.html"

    def get(self, request, pk):
        harassment_report = Harassment_report.objects.get(pk=pk) # 一覧画面で選択したハラスメント報告を取得
        print('🔥')
        print(harassment_report)
        return render(request, self.template_name, {"harassment_report": harassment_report})


# アカウント情報確認画面
class AccountInfoView(LoginRequiredMixin,TemplateView):
    template_name = 'account_info.html'

# ID確認
class CheckIdView(TemplateView):
    template_name = "check_id.html"
    form_class = CheckIdForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            account_id = form.cleaned_data['account_id'] # 入力されたアカウントID
            user = Users.objects.filter(account_id=account_id).first()  # 条件に一致するユーザー情報を取得

            # 入力されたアカウントIDが存在した場合
            if account_id == user.account_id:
                self.request.session['account_id'] = user.account_id  # アカウントIDをセッションに保存
                # スーパーユーザーの場合
                if user.superuser_flag and user.user_flag:
                    return redirect("app:send_email")
                # ユーザーの場合
                elif not user.superuser_flag and user.user_flag:
                    return redirect("app:send_superuser")
            
            # 入力されたアカウントIDが存在しない場合
            else:
                return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {"form": form})
        
# Email送信
class SendEmailView(TemplateView):
    template_name = "forget_password.html"
    form_class = SendEmailForm
    success_url = reverse_lazy("app:pw_send_comp")

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'] # 入力されたメールアドレス
            subject = '件名'  # メールの件名
            message = 'パスワード変更URL'  # メールの内容
            send_email(email, subject, message)  # メール送信
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})

# PWリセット要請
class SendSuperuserView(TemplateView):
    template_name = "forget_password.html"
    form_class = SendSuperuserForm
    success_url = reverse_lazy("app:pw_send_comp")


    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        account_id = self.request.session.get('account_id') # ID確認で入力したアカウントIDを取得

        form = self.form_class(request.POST)
        if form.is_valid():
            superuser_id = form.cleaned_data['superuser_name'] # 選択したスーパーユーザー
            user = Users.objects.filter(account_id=account_id).first()  # 条件に一致するユーザーを取得
            notification = Notification.objects.create(
                sender_name = user.account_name, # 送信元を登録
                company_id = user.company.id, # 企業IDを登録
                destination = superuser_id, # 送り先を登録
                genre = 1, # ジャンルを1に設定
            )
            notification.save() # 保存
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})
        
# メール送信完了
class PwSendCompleteView(TemplateView):
    template_name = "pw_send_comp.html"
    
#パスワード変更画面
class PasswordChangeView(LoginRequiredMixin,TemplateView):
    template_name = 'password_change.html'  # パスワード変更用のテンプレート
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("app:pw_change_complete")
    
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        user = Users.objects.get(id=request.user.id) # ログインユーザーの情報を取得
        if form.is_valid():
            new_password = form.cleaned_data['new_password'] # 入力されたパスワード
            new_password = make_password(new_password) # 入力されたパスワードをハッシュ化      
            user.password = new_password # パスワードを更新
            user.save() # 保存
            update_session_auth_hash(request, user) # ログインを継続
            return redirect(self.success_url) 
        return render(request, self.template_name, {"form": form})  

# PWリセット完了画面
class PwChangeCompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'pw_complete.html'  # パスワード変更完了用のテンプレート

# PWリセット通知
class NotificationView(LoginRequiredMixin,TemplateView):
    template_name = 'notification.html'

    def get(self, request):
        # スーパーユーザーの場合
        if request.user.superuser_flag:
            # 条件に一致する通知を取得
            notifications = Notification.objects.filter(
                company_id=request.user.company.id,
                destination=request.user.account_name,
                genre='1',
                is_read=False
            )
        # 管理者の場合  
        elif request.user.admin_flag:
            # 条件に一致する通知を取得
            notifications = Notification.objects.filter(
                genre='2',
                is_read=False
            )
        paginator = Paginator(notifications, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj})
    
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
class PasswordReset(LoginRequiredMixin, TemplateView):
    template_name = 'confirm_pw_reset.html'
    success_url = reverse_lazy('app:notification')
    
    def get(self, request, sender_name):
        user = Users.objects.get(account_name=sender_name) # 選択したユーザーの情報を取得
        return render(request, self.template_name, {"object": user})
    
    def post(self, request, sender_name):
        if request.method == 'POST':
            user = Users.objects.get(account_name=sender_name) # 選択したユーザーの情報を取得
            notification = Notification.objects.get(sender_name=sender_name) # 選択した報告の情報を取得
            user.password = user.start_password # 現在のPWを初期パスワードに変更
            notification.is_read = True # リセットした通知をTrueに変更
            user.save()
            notification.save()
            return redirect(self.success_url)
        return render(request, self.template_name)
    
# スーパーユーザー削除要請
class SendSuperuserDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'send_superuser_delete.html'
    success_url = reverse_lazy('app:user_list')

    def get(self, request, pk):
        user = Users.objects.get(id=pk) # 選択したスーパーユーザーの情報を取得
        return render(request, self.template_name, {"object": user})
    
    def post(self, request, pk):
        if request.method == 'POST':
            user = Users.objects.get(id=pk) # 選択したスーパーユーザーの情報を取得
            notification = Notification.objects.create(
                    sender_name = user.account_name, # 送り元を登録
                    company_id = user.company.id, # 企業IDを登録
                    destination = 'admin', # 送り先を登録
                    genre = 2, # ジャンルを2に設定
                )
            notification.save() # 保存
            return redirect(self.success_url)
        return render(request, self.template_name, {"object": user})
    
# スーパーユーザー削除
class SuperuserDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'superuser_confirm_delete.html'
    success_url = reverse_lazy('app:notification')
    
    def get(self, request, sender_name):
        delete_user = Users.objects.filter(account_name=sender_name).first() # 選択したユーザーの情報を取得
        return render(request, self.template_name, {"object": delete_user})
    
    def post(self, request, sender_name):
        if request.method == 'POST':
            delete_user = Users.objects.filter(account_name=sender_name).first() # 選択したユーザーの情報を取得
            notifications = Notification.objects.filter(sender_name=sender_name) # 選択した報告の情報を取得
            delete_user.delete() # 選択したユーザーを削除
            for notification in notifications:
                notification.is_read = True # is_readをTrue
                notification.save() # 保存
            return redirect(self.success_url)
        return render(request, self.template_name, {"object": delete_user})

# エラー
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_403_view(request, exception):
    return render(request, '403.html', status=403)

def custom_500_view(request):
    return render(request, '500.html', status=500)