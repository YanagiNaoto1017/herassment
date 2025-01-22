from pyexpat.errors import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from .forms import AdminSignUpForm,CompanySignUpForm,SuperUserSignUpForm,LoginForm,UserSignUpForm,HarassmentReportForm,ErrorReportForm,CheckIdForm,SendEmailForm,SendSuperuserForm,DetectionForm,CustomPasswordChangeForm,SearchForm,MailPWChangeForm,MailChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Company,Users,Error_report,Text,Harassment_report,Dictionary,Notification,HarassmentReportImage
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseForbidden

import jwt
import spacy
from django.core.mail import send_mail
from django.conf import settings
from transformers import BertForSequenceClassification, BertTokenizer
import torch
import torch.nn.functional as F
from decimal import Decimal, ROUND_DOWN

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
class SignupView(CreateView):
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
        admin_list = Users.objects.filter(admin_flag=True).order_by('-created_at')  # 管理者を取得
        paginator = Paginator(admin_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            search_text = form.cleaned_data.get('search_text')  # 入力されたテキスト
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日

            admin_list = Users.objects.filter(admin_flag=True).order_by('-created_at')

            filters = Q()  # 空のQオブジェクトを作成

            if search_text:
                filters &= Q(account_name__icontains=search_text) | Q(account_id__icontains=search_text)
            if start_date:
                filters &= Q(created_at__gte=start_date)
            if end_date:
                end_date = end_date + timedelta(days=1) # 終了日を1日加算
                filters &= Q(created_at__lte=end_date)

            # フィルタを適用してクエリセットを取得
            admin_list = admin_list.filter(filters).order_by('-created_at')

            paginator = Paginator(admin_list, 10) # 1ページ当たり10件
            page_number = request.GET.get('page') # 現在のページ番号を取得
            page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})

# 企業一覧画面
class CompanyListView(LoginRequiredMixin,TemplateView):
    template_name = "company_list.html"
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        company_list = Company.objects.all().order_by('-created_at') # 企業を取得
        paginator = Paginator(company_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj,"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            search_text = form.cleaned_data.get('search_text')  # 入力されたテキスト
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日

            company_list = Company.objects.all().order_by('-created_at')

            filters = Q()  # 空のQオブジェクトを作成

            if search_text:
                filters &= Q(company_name__icontains=search_text) | Q(id__icontains=search_text)
            if start_date:
                filters &= Q(created_at__gte=start_date)
            if end_date:
                end_date = end_date + timedelta(days=1) # 終了日を1日加算
                filters &= Q(created_at__lte=end_date)

            # フィルタを適用してクエリセットを取得
            company_list = company_list.filter(filters).order_by('-created_at')

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
            user_list = Users.objects.filter(user_flag=True,company=request.user.company).order_by('-created_at')  # 条件に一致するユーザーを取得
        # 管理者の場合
        elif request.user.admin_flag:
            user_list = Users.objects.filter(user_flag=True).order_by('-created_at')  # ユーザーを取得

        paginator = Paginator(user_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
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
                user_list = Users.objects.filter(user_flag=True,company=request.user.company).order_by('-created_at')

                filters = Q()  # 空のQオブジェクトを作成

                if search_text:
                    filters &= Q(account_name__icontains=search_text)
                if start_date:
                    filters &= Q(created_at__gte=start_date)
                if end_date:
                    end_date = end_date + timedelta(days=1) # 終了日を1日加算
                    filters &= Q(created_at__lte=end_date)

                # フィルタを適用してクエリセットを取得
                user_list = user_list.filter(filters)

            # 管理者の場合
            elif request.user.admin_flag:
                user_list = Users.objects.filter(user_flag=True).order_by('-created_at')
                
                filters = Q()  # 空のQオブジェクトを作成

                if search_text:
                    filters &= Q(account_name__icontains=search_text) | Q(account_id__icontains=search_text) | Q(company__company_name__icontains=search_text)
                if start_date:
                    filters &= Q(created_at__gte=start_date)
                if end_date:
                    end_date = end_date + timedelta(days=1) # 終了日を1日加算
                    filters &= Q(created_at__lte=end_date)

                # フィルタを適用してクエリセットを取得
                user_list = user_list.filter(filters).order_by('-created_at')

            paginator = Paginator(user_list, 10) # 1ページ当たり10件
            page_number = request.GET.get('page') # 現在のページ番号を取得
            page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})


# エラー一覧画面
class ErrorReportListView(LoginRequiredMixin,TemplateView):
    template_name = "error_list.html"
    form_class = SearchForm

    def get(self, request):
        form = self.form_class
        error_list = Error_report.objects.all().order_by('-report_time') # エラー報告を取得
        paginator = Paginator(error_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日

            error_report = Error_report.objects.all().order_by('-report_time')

            filters = Q()  # 空のQオブジェクトを作成

            if start_date:
                filters &= Q(report_time__gte=start_date)
            if end_date:
                end_date = end_date + timedelta(days=1) # 終了日を1日加算
                filters &= Q(report_time__lte=end_date)

            # フィルタを適用してクエリセットを取得
            error_list = error_report.filter(filters).order_by('-report_time')

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
        form = self.form_class(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text'] # 入力されたテキスト

            # 日本語BERTモデルとトークナイザーをロード
            model_name = "cl-tohoku/bert-base-japanese"
            model = BertForSequenceClassification.from_pretrained(model_name)
            tokenizer = BertTokenizer.from_pretrained(model_name)

            # テキストをトークン化
            input = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)

             # モデルで予測
            with torch.no_grad():
                logits = model(**input).logits

            # softmaxを適用して確率を計算
            probabilities = F.softmax(logits, dim=-1)

            # 各クラスの確率（感情スコア）
            positive_prob = probabilities[0][1].item()  # Positiveクラスの確率
            negative_prob = probabilities[0][0].item()  # Negativeクラスの確率

            # 予測された感情（0 = Negative, 1 = Positive）
            predicted_class = torch.argmax(logits, dim=1).item()

            sentiment = "Positive" if predicted_class == 1 else "Negative"
            print('🔥')
            print(f"Text: {input_text}")
            print(f"Sentiment: {sentiment}")
            print(f"Positive Probability: {positive_prob:.4f}")
            print(f"Negative Probability: {negative_prob:.4f}")
            print("-" * 50)
            
            nlp = spacy.load("ja_core_news_sm") # モデルのロード
            doc = nlp(input_text) # 入力テキストを単語に分割

            keywords = Dictionary.objects.values_list('keyword', flat=True) # 辞書からキーワードを取得

            detected_words = [token.text for token in doc if token.text in keywords] # 辞書との照合

            # 検出単語がある場合
            if detected_words:
                print('検出あり')
                print(detected_words)

                text_instance = Text.objects.create(
                    input_text=input_text, # 入力されたテキストを保存
                    harassment_flag=True, # ハラスメントフラグをTrue
                    detected_words=', '.join(detected_words) if detected_words else None
                )

                if sentiment == "Positive":
                    sentiment = "ポジティブ"
                elif sentiment == "Negative":
                    sentiment = "ネガティブ"

                # 小数点第3位まで表示
                positive_prob = Decimal(positive_prob*100).quantize(Decimal('0.01'))
                negative_prob = Decimal(negative_prob*100).quantize(Decimal('0.01'))

                return render(request, self.template_name, {
                    'form': form,
                    'text': text_instance,
                    'sentiment': sentiment,
                    'positive_prob': positive_prob,
                    'negative_prob': negative_prob,
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
            harassment_report.save()
            images = request.FILES.getlist('images')  # 複数画像を取得
            for img in images:
                HarassmentReportImage.objects.create(report=harassment_report, image=img)  # 画像を保存
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form})
    
# ハラスメント一覧画面
class HarassmentReportListView(LoginRequiredMixin,TemplateView):
    template_name = "harassment_list.html"
    form_class = SearchForm

    def get(self, request):
        harassment_list = Harassment_report.objects.filter(company_id=request.user.company.id).order_by('-report_time') # 同じ企業IDのハラスメント報告を取得
        paginator = Paginator(harassment_list, 10) # 1ページ当たり10件
        page_number = request.GET.get('page') # 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # 検索フォームで入力されたものを取得
            start_date = form.cleaned_data.get('start_date')    # 開始日
            end_date = form.cleaned_data.get('end_date')        # 終了日

            harassment_list = Harassment_report.objects.filter(company_id=request.user.company.id).order_by('-report_time')

            filters = Q()  # 空のQオブジェクトを作成

            if start_date:
                filters &= Q(report_time__gte=start_date)
            if end_date:
                filters &= Q(report_time__lte=end_date)

            # フィルタを適用してクエリセットを取得
            harassment_list = harassment_list.filter(filters).order_by('-report_time')

            paginator = Paginator(harassment_list, 10) # 1ページ当たり10件
            page_number = request.GET.get('page') # 現在のページ番号を取得
            page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {"page_obj": page_obj, "form": form})
    
# ハラスメント詳細画面
class HarassmentDetailView(LoginRequiredMixin, TemplateView):
    template_name = "harassment_detail.html"

    def get(self, request, pk):
        harassment_report = Harassment_report.objects.get(pk=pk) # 一覧画面で選択したハラスメント報告を取得
        harassment_report_img = HarassmentReportImage.objects.filter(report=harassment_report) # ハラスメント報告に紐づく画像を取得
        return render(request, self.template_name, {"harassment_report": harassment_report, "harassment_report_img": harassment_report_img})


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
            if user:
                self.request.session['account_id'] = user.account_id  # アカウントIDをセッションに保存
                # スーパーユーザーの場合
                if user.superuser_flag:
                    email = user.email
                    print(f'{email}')
                    send_email(email, user)
                    return redirect("app:send_email")
                # ユーザーの場合
                if user. user_flag and not user.superuser_flag:
                    return redirect("app:send_superuser")
            
            # 入力されたアカウントIDが存在しない場合
            else:
                return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {"form": form})
        
# Email送信
def send_email(to_email, user):
    token = jwt.encode(
        {'user_id': user.id, 'exp': timezone.now() + timezone.timedelta(hours=1)},
        settings.SECRET_KEY,
        algorithm='HS256'
    )
    url = f'http://127.0.0.1:8000/mail_PWchange/?token={token}'
    subject = 'へらすめんと　パスワード再設定'  # メールの件名
    message = f'パスワード再設定用のURLです: {url}'  # 内容
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
    )

class SendEmailView(TemplateView):
    template_name = "forget_password.html"
    form_class = SendEmailForm
    success_url = reverse_lazy("app:pw_send_comp")

    def get(self, request):
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
        
# メール送信完了
class PwSendCompleteView(TemplateView):
    template_name = "pw_send_comp.html"
    
# パスワード変更画面
class PasswordChangeView(LoginRequiredMixin, TemplateView):
    template_name = 'password_change.html'  # パスワード変更用のテンプレート
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("app:pw_change_complete")
    
    def get(self, request):
        form = self.form_class()
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

        user = Users.objects.get(id=request.user.id) # ログインユーザーの情報を取得
        if form.is_valid():
            new_password = form.cleaned_data['new_password'] # 入力されたパスワード
            new_password = make_password(new_password) # 入力されたパスワードをハッシュ化      
            user.password = new_password # パスワードを更新
            user.update_at = timezone.now() # 更新日時を更新
            user.save() # 保存
            update_session_auth_hash(request, user) # ログインを継続
            return redirect(self.success_url) 
        return render(request, self.template_name, {"form": form})  
    
# メールアドレス変更画面
class EmailChangeView(LoginRequiredMixin,TemplateView):
    template_name = 'email_change.html'  # メールアドレス変更用のテンプレート
    form_class = MailChangeForm
    success_url = reverse_lazy("app:email_change_comp")
    
    def get(self, request):
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

# PWリセット完了画面
class PwChangeCompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'pw_complete.html'  # パスワード変更完了用のテンプレート

# メールアドレス変更完了画面
class EmailChangeCompleteView(LoginRequiredMixin,TemplateView):
    template_name = 'email_change_comp.html'  # メールアドレス変更完了用のテンプレート

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
        user = Users.objects.filter(account_name=sender_name).first() # 選択したユーザーの情報を取得
        if not user:
            return render(request, self.template_name, {"error": "ユーザーが見つかりません。"})
        return render(request, self.template_name, {"object": user})
    
    def post(self, request, sender_name):
        if request.method == 'POST':
            user = Users.objects.filter(account_name=sender_name).first() # 選択したユーザーの情報を取得
            if not user:
                return render(request, self.template_name, {"error": "ユーザーが見つかりません。"})
            
            notification = Notification.objects.filter(sender_name=sender_name) # 選択した報告の情報を取得
            if not notification.exists():
                return render(request, self.template_name, {"error": "通知が見つかりません。"})
            
            user.password = user.start_password # 現在のPWを初期パスワードに変更
            user.save()
            notification.update(is_read=True)
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
            else:
                user = request.user  # ログインしたユーザーを取得
                user.set_password(new_password)  # パスワードをハッシュ化して保存
                user.save()  # ユーザーを保存
                print("パスワード変更完了")
                return redirect(self.success_url)  # 成功した場合のリダイレクト

        # フォームが無効な場合、またはエラーがある場合は再表示
        return render(request, self.template_name, {'form': form})

class MailPwCompleteView(TemplateView):
    template_name = 'mail_PWcomp.html'  # パスワード変更完了用のテンプレート



# エラー
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_403_view(request, exception):
    return render(request, '403.html', status=403)

def custom_500_view(request):
    return render(request, '500.html', status=500)