from django.contrib.auth import login, update_session_auth_hash
from django.views.generic import TemplateView, CreateView, DeleteView
from pyexpat.errors import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import (
    AdminSignUpForm,
    CompanySignUpForm,
    SuperUserSignUpForm,
    LoginForm,
    UserSignUpForm,
    HarassmentReportForm,
    ErrorReportForm,
    CheckIdForm,
    SendEmailForm,
    SendSuperuserForm,
    DetectionForm,
    CustomPasswordChangeForm,
    SearchForm,
    MailPWChangeForm,
    MailChangeForm,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users,Error_report,Text,Harassment_report,Dictionary,Notification,HarassmentReportImage
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponseForbidden

import re
import jwt
import spacy
from django.core.mail import send_mail
from django.conf import settings

# ホーム画面表示
class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "index.html"

# 管理者新規登録
class SignupView(CreateView):
    form_class = AdminSignUpForm
    template_name = "admin_signup.html"
    success_url = reverse_lazy("app:complete")

    def get(self, request, *args, **kwargs):
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        return super().get(request, *args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        return super().get(request, *args, **kwargs)

# スーパーユーザー登録
class SuperUserSignupView(LoginRequiredMixin,CreateView):
    form_class = SuperUserSignUpForm
    template_name = "superuser_signup.html"
    success_url = reverse_lazy("app:complete")

    def get(self, request, *args, **kwargs):
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        return super().get(request, *args, **kwargs)

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

### 一覧画面 ###

# 1ページの表示件数を10件に設定ための関数
def pagenator(request, queryset):
    paginator = Paginator(queryset, 10) # 1ページ当たり10件
    page_number = request.GET.get('page') # 現在のページ番号を取得
    page_obj = paginator.get_page(page_number)
    return page_obj

# 検索条件をQオブジェクトとして構築する関数
def build_search_filters(search_text, start_date, end_date, name_field, id_field, company_field, date_field):
    filters = Q()
    if search_text:
        search_conditions = Q(**{f"{name_field}__icontains": search_text})
        if id_field:
            search_conditions |= Q(**{f"{id_field}__icontains": search_text})
        if company_field:
            search_conditions |= Q(**{f"{company_field}__icontains": search_text})
        filters &= search_conditions
    if start_date:
        filters &= Q(**{f"{date_field}__gte": start_date})
    if end_date:
        end_date += timedelta(days=1)  # 終了日を含めるため+1日
        filters &= Q(**{f"{date_field}__lte": end_date})
    return filters

# 管理者一覧画面
class AdminListView(LoginRequiredMixin,TemplateView):
    template_name = "admin_list.html"
    form_class = SearchForm

    def get(self, request):
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        form = self.form_class
        admin_list = Users.objects.filter(admin_flag=True).order_by('-created_at')  # 管理者を取得
        page_obj = pagenator(request, admin_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            search_text = form.cleaned_data.get('search_text')  # 入力されたテキスト
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日
            filters = build_search_filters(search_text, start_date, end_date, 'account_name', 'account_id', None, 'created_at')
            # フィルタを適用してクエリセットを取得
            admin_list = Users.objects.filter(admin_flag=True).filter(filters).order_by('-created_at')
            page_obj = pagenator(request, admin_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})

# 企業一覧画面
class CompanyListView(LoginRequiredMixin,TemplateView):
    template_name = "company_list.html"
    form_class = SearchForm

    def get(self, request):
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        form = self.form_class
        company_list = Company.objects.all().order_by('-created_at') # 企業を取得
        page_obj = pagenator(request, company_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj,"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            search_text = form.cleaned_data.get('search_text')  # 入力されたテキスト
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日
            filters = build_search_filters(search_text, start_date, end_date, 'company_name', 'id', None , 'created_at')
            # フィルタを適用してクエリセットを取得
            company_list = Company.objects.filter(filters).order_by('-created_at')
            page_obj = pagenator(request, company_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj,"form": form})

# ユーザー一覧画面
class UserListView(LoginRequiredMixin,TemplateView):
    template_name = "user_list.html"
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        # スーパーユーザーの場合
        if request.user.superuser_flag:
            user_list = Users.objects.filter(user_flag=True,company=request.user.company).order_by('-created_at')
        # 管理者の場合
        elif request.user.admin_flag:
            user_list = Users.objects.filter(user_flag=True).order_by('-created_at')
        else:
            return HttpResponseForbidden(render(request, '403.html'))
        page_obj = pagenator(request, user_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            search_text = form.cleaned_data.get('search_text')  # 入力されたテキスト
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日
            # スーパーユーザーの場合
            if request.user.superuser_flag:
                filters = build_search_filters(search_text, start_date, end_date, 'account_name', None, None, 'created_at')
                # フィルタを適用してクエリセットを取得
                user_list = Users.objects.filter(user_flag=True,company=request.user.company).filter(filters).order_by('-created_at')
            # 管理者の場合
            elif request.user.admin_flag:
                filters = build_search_filters(search_text, start_date, end_date, 'account_name', 'account_id', 'company__company_name', 'created_at')
                # フィルタを適用してクエリセットを取得
                user_list = Users.objects.filter(user_flag=True).filter(filters).order_by('-created_at')
            page_obj = pagenator(request, user_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})


# エラー一覧画面
class ErrorReportListView(LoginRequiredMixin,TemplateView):
    template_name = "error_list.html"
    form_class = SearchForm

    def get(self, request):
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        form = self.form_class
        error_list = Error_report.objects.all().order_by('-report_time') # エラー報告を取得
        page_obj = pagenator(request, error_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日
            filters = build_search_filters(None, start_date, end_date, None, None, None, 'report_time')
            # フィルタを適用してクエリセットを取得
            error_list = Error_report.objects.filter(filters).order_by('-report_time')
            page_obj = pagenator(request, error_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})

# ハラスメント一覧画面
class HarassmentReportListView(LoginRequiredMixin,TemplateView):
    template_name = "harassment_list.html"
    form_class = SearchForm

    def get(self, request):
        if not request.user.superuser_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        harassment_list = Harassment_report.objects.filter(company_id=request.user.company.id).order_by('-report_time')
        page_obj = pagenator(request, harassment_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日
            filters = build_search_filters(None, start_date, end_date, None, None, None, 'report_time')
            # フィルタを適用してクエリセットを取得
            harassment_list = Harassment_report.objects.filter(company_id=request.user.company.id).filter(filters).order_by('-report_time')
            page_obj = pagenator(request, harassment_list) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})

# ハラスメント詳細画面
class HarassmentDetailView(LoginRequiredMixin, TemplateView):
    template_name = "harassment_detail.html"

    def get(self, request, pk):
        if not request.user.superuser_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        harassment_report = Harassment_report.objects.get(pk=pk) # 一覧画面で選択したハラスメント報告を取得
        harassment_report_img = HarassmentReportImage.objects.filter(report=harassment_report) # ハラスメント報告に紐づく画像を取得
        return render(request, self.template_name, {"harassment_report": harassment_report, "harassment_report_img": harassment_report_img})

# 検出画面
class DetectionView(LoginRequiredMixin,TemplateView):
    template_name = 'detection.html'
    form_class = DetectionForm

    def get(self, request):
        if not request.user.user_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text'] # 入力されたテキスト
            
            nlp = spacy.load("ja_core_news_sm") # モデルのロード
            doc = nlp(input_text) # 入力テキストを単語に分割
            print(doc)

            keywords = Dictionary.objects.values_list('keyword', flat=True) # 辞書からキーワードを取得
            print(keywords)

            detected_words = [token.text for token in doc if token.text in keywords] # 辞書との照合
            print(detected_words)

            # 検出単語がある場合
            if detected_words:
                print('検出あり')
                print(detected_words)

                text_instance = Text.objects.create(
                    input_text=input_text, # 入力されたテキストを保存
                    harassment_flag=True, # ハラスメントフラグをTrue
                    detected_words=', '.join(detected_words) if detected_words else None
                )

                return render(request, self.template_name, {
                    'form': form,
                    'text': text_instance,
                    })
            
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

    def get(self, request, *args, **kwargs):
        if not request.user.superuser_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        return super().get(request, *args, **kwargs)

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
        if not request.user.user_flag:
            return HttpResponseForbidden(render(request, '403.html'))
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
        if not request.user.user_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        form = self.form_class
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            harassment_report = form.save(commit=False)  # フォームの save を呼び出す
            harassment_report.company_id = request.user.company.id # ログインユーザーの企業IDを登録
            harassment_report.save()
            images = request.FILES.getlist('images')  # 複数画像を取得
            for img in images:
                HarassmentReportImage.objects.create(report=harassment_report, image=img)  # 画像を保存
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})

# アカウント情報確認画面
class AccountInfoView(LoginRequiredMixin,TemplateView):
    template_name = 'account_info.html'

    def get(self, request, *args, **kwargs):
        if not request.user.user_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        return super().get(request, *args, **kwargs)

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
            if 'user_type' in request.session:
                del request.session['user_type']

            # 入力されたアカウントIDが存在した場合
            if user:
                self.request.session['account_id'] = user.account_id  # アカウントIDをセッションに保存
                # スーパーユーザーの場合
                if user.superuser_flag:
                    email = user.email
                    print(f'{email}')
                    send_email(email, user)
                    print("スーパーユーザーと判断")
                    request.session['user_type'] = 'super'
                    return redirect("app:send_email")
                # ユーザーの場合
                if user. user_flag and not user.superuser_flag:
                    print("ユーザーと判断")
                    request.session['user_type'] = 'user'
                    return redirect("app:send_superuser")
            
            # 入力されたアカウントIDが存在しない場合
            else:
                return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {"form": form})

# メール送信関数
def send_email(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,  # 送信者のメールアドレス
        [to_email],  # 受信者のメールアドレス
        fail_silently=False,
    )
        
# Email送信
def send_email(to_email, user):
    token = jwt.encode(
        {'user_id': user.id, 'exp': timezone.now() + timezone.timedelta(hours=1)},
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    url = f'http://127.0.0.1:8000/mail/password_change/?token={token}'
    subject = 'へらすめんと　パスワード再設定'  # メールの件名
    message = f'パスワード再設定用のURLです: {url}'  # 内容
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )

# パスワード再設定時のメール送信
class SendEmailView(TemplateView):
    template_name = "forget_password.html"
    form_class = SendEmailForm
    success_url = reverse_lazy("app:pw_send_comp")

    def get(self, request):
        account_id = request.session.get('account_id')
        user = Users.objects.filter(account_id=account_id).first()
        if not user or not user.superuser_flag:
            return redirect("app:check_id")
        
        form = self.form_class
        return render(request, self.template_name, {"form": form})

        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  # 入力されたメールアドレス
            
            try:
                user = Users.objects.get(email=email)  # メールアドレスからユーザーを取得
                send_email(email, user)  # メール送信
                return redirect(self.success_url)
            except Users.DoesNotExist:
                form.add_error('email', "このメールアドレスは登録されていません。")
        
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
        user = Users.objects.filter(account_id=account_id).first()

        if not user:
            return redirect("app:check_id")

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
        return render(self.template_name, {"form": form})

#アカウント情報からのパスワード変更画面
class PasswordChangeView(LoginRequiredMixin,TemplateView):
    template_name = 'password_change.html'  # パスワード変更用のテンプレート
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("app:pw_change_complete")
    
    def get(self, request):
        if not request.user.user_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        # パスワードフィールドの入力チェック
        new_password = request.POST.get('new_password', '')
        new_password2 = request.POST.get('new_password2', '')

        if not new_password or not new_password2:
            form.add_error(None, "どちらも入力してください。")  # フォーム全体にエラーメッセージを追加
        elif form.is_valid():
            # パスワードの長さをチェック
            if len(new_password) < 4:
                form.add_error('new_password', "パスワードは4文字以上でなければなりません。")
            elif new_password != new_password2:
                form.add_error('new_password2', "パスワードが一致しません。")
            elif re.match(r'^[a-zA-Z0-9]+$', new_password) is None:
                # 半角英数字のみのチェック
                form.add_error('new_password', "パスワードは半角英数字のみでなければなりません。")
            else:
                user = request.user  # ログインしたユーザーを取得
                user.set_password(new_password)  # パスワードをハッシュ化して保存
                user.save()  # ユーザーを保存
                print("パスワード変更完了")

                # セッションの認証情報を更新
                update_session_auth_hash(request, user)  # ログインを継続
                return redirect(self.success_url)  # 成功した場合のリダイレクト

        # フォームが無効な場合、またはエラーがある場合は再表示
        return render(request, self.template_name, {'form': form}) 
    
# メールアドレス変更画面
class EmailChangeView(LoginRequiredMixin,TemplateView):
    template_name = 'email_change.html'  # メールアドレス変更用のテンプレート
    form_class = MailChangeForm
    success_url = reverse_lazy("app:email_change_comp")
    
    def get(self, request):
        if not request.user.superuser_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        user = Users.objects.get(id=request.user.id) # ログインユーザーの情報を取得
        if form.is_valid():
            new_email = form.cleaned_data['new_email'] # 入力されたメールアドレス
            user.email = new_email # メールアドレスを更新
            user.update_at = timezone.now() # 更新日時を更新
            user.save() # 保存
            return redirect(self.success_url) 
        return render(request, self.template_name, {"form": form})

# 通知
class NotificationView(LoginRequiredMixin,TemplateView):
    template_name = 'notification.html'

    def get(self, request):
        # スーパーユーザーの場合
        if request.user.superuser_flag:
            # 条件に一致する通知を取得
            notifications = Notification.objects.filter(company_id=request.user.company.id,).order_by('-created_at')

        # 管理者の場合  
        elif request.user.admin_flag:
            # 条件に一致する通知を取得
            notifications = Notification.objects.filter(
                genre='2',
                is_read=False
            ).order_by('-created_at')
        else:
            return HttpResponseForbidden(render(request, '403.html'))
        page_obj = pagenator(request, notifications) # 1ページの表示件数を設定
        return render(request, self.template_name, {"page_obj": page_obj})
    
# ユーザー削除
class UserDeleteView(DeleteView):
    model = Users
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('app:user_list')

    def get(self, request, *args, **kwargs):
        if not request.user.superuser_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        return super().get(request, *args, **kwargs)
    
    def post(self, request, pk):
        if request.method == 'POST':
            user = Users.objects.get(id=pk) # 選択したユーザーの情報を取得
            # 削除するユーザーを通知テーブルに追加
            Notification.objects.create(
                sender_name = user.account_name,
                company_id = request.user.company.id,
                destination = request.user.account_name,
                genre = '2',
                is_read = True,
            )
            user.delete() # 選択したユーザーを削除
        return redirect(self.success_url)

# 管理者削除
class AdminDeleteView(DeleteView):
    model = Users
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('app:admin_list')

    def get(self, request, *args, **kwargs):
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        return super().get(request, *args, **kwargs)

# 企業削除
class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'company_confirm_delete.html'
    success_url = reverse_lazy('app:company_list')

    def get(self, request, *args, **kwargs):
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        return super().get(request, *args, **kwargs)

# パスワードリセット
class PasswordReset(LoginRequiredMixin, TemplateView):
    template_name = 'confirm_pw_reset.html'
    success_url = reverse_lazy('app:notification')
    
    def get(self, request, sender_name):
        if not request.user.superuser_flag:
            return HttpResponseForbidden(render(request, '403.html'))
        
        user = Users.objects.filter(account_name=sender_name).first() # 選択したユーザーの情報を取得
        if not user:
            return render(request, self.template_name, {"error": "ユーザーが見つかりません。"})
        return render(request, self.template_name, {"object": user})
    
    def post(self, request, sender_name):
        if request.method == 'POST':
            user = Users.objects.filter(account_name=sender_name).first() # 選択したユーザーの情報を取得
            if not user:
                return render(request, self.template_name, {"error": "ユーザーが見つかりません。"})
            user.password = user.start_password # 現在のPWを初期パスワードに変更
            user.save()
            
            notification = Notification.objects.filter(sender_name=sender_name) # 選択した報告の情報を取得
            if not notification.exists():
                return render(request, self.template_name, {"error": "通知が見つかりません。"})
            notification.update(is_read=True)
            
            return redirect(self.success_url)
        return render(request, self.template_name)
    
# スーパーユーザー削除要請
class SendSuperuserDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'send_superuser_delete.html'
    success_url = reverse_lazy('app:user_list')

    def get(self, request, pk):
        if not request.user.superuser_flag:
            return HttpResponseForbidden(render(request, '403.html'))
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
        if not request.user.admin_flag:
            return HttpResponseForbidden(render(request, '403.html'))
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

# メールからのパスワード変更画面
class MailPWChangeView(TemplateView):
    template_name = 'mail_PWchange.html'
    success_url = reverse_lazy('app:mail_PWcomp')

    def get(self, request):
        token = request.GET.get('token')
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = Users.objects.get(id=payload['user_id'])
                login(request, user)  # ユーザーをログインさせる
                form = MailPWChangeForm()  # フォームのインスタンスを作成
                return render(request, self.template_name, {'form': form})
            except (jwt.ExpiredSignatureError, jwt.DecodeError, Users.DoesNotExist):
                return HttpResponseForbidden("無効なトークンです。")
        return redirect('app:login')  # トークンがない場合はログインページにリダイレクト

    def post(self, request):
        form = MailPWChangeForm(request.POST)
        
        # パスワードフィールドの入力チェック
        new_password = request.POST.get('new_password', '')
        new_password2 = request.POST.get('new_password2', '')

        if not new_password or not new_password2:
            form.add_error(None, "どちらも入力してください。")  # フォーム全体にエラーメッセージを追加
        elif form.is_valid():
            # パスワードの長さをチェック
            if len(new_password) < 4:
                form.add_error('new_password', "パスワードは4文字以上でなければなりません。")
            elif new_password != new_password2:
                form.add_error('new_password2', "パスワードが一致しません。")
            elif re.match(r'^[a-zA-Z0-9]+$', new_password) is None:
                # 半角英数字のみのチェック
                form.add_error('new_password', "パスワードは半角英数字のみでなければなりません。")
            else:
                user = request.user  # ログインしたユーザーを取得
                user.set_password(new_password)  # パスワードをハッシュ化して保存
                user.save()  # ユーザーを保存
                print("パスワード変更完了")
                return redirect(self.success_url)  # 成功した場合のリダイレクト

        # フォームが無効な場合、またはエラーがある場合は再表示
        return render(request, self.template_name, {'form': form})


### 完了画面 ###

# 登録完了画面
class CompleteView(LoginRequiredMixin,TemplateView):
    template_name = "complete.html"

# 報告完了画面
class ReportCompleteView(LoginRequiredMixin,TemplateView):
    template_name = "report_complete.html"

# 削除完了画面
class DeleteCompleteView(LoginRequiredMixin,TemplateView):
    template_name = "delete_complete.html"

# PWリセット完了画面
class PwChangeCompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'pw_complete.html'  # パスワード変更完了用のテンプレート

# メールアドレス変更完了画面
class EmailChangeCompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'email_change_comp.html'  # メールアドレス変更完了用のテンプレート

# メール送信完了
class PwSendCompleteView(TemplateView):
    template_name = "pw_send_comp.html"

# メールからのパスワード変更完了画面

class MailPwCompleteView(TemplateView):
    template_name = 'mail_PWcomp.html'  # パスワード変更完了用のテンプレート


### エラーハンドリング ###

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_403_view(request, exception):
    return render(request, '403.html', status=403)

def custom_500_view(request):
    return render(request, '500.html', status=500)