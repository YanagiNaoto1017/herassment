from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Admin,Company,Users,Harassment_report,Error_report
from django.contrib.auth.hashers import make_password

# 管理者新規登録
class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ("account_id","email",)
        labels = {'account_id':'ID', 'email':'メールアドレス'}

# 管理者ログイン
class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = Admin

# 企業登録
class CompanySignUpForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("id","company_name",)
        labels = {'id':'企業ID', 'company_name':'企業名'}

# スーパーユーザー登録
class SuperUserSignUpForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ("account_id","company","email")
        labels = {'account_id':'ID', 'company':'企業名','email':'メールアドレス'}

    def save(self, commit=True):
        # ユーザーインスタンスを作成
        user = super().save(commit=False)
        
        # パスワードがハッシュ化されていなければハッシュ化
        if not user.password.startswith('pbkdf2_sha256$'):  # ハッシュ化されていない場合
            user.password = make_password(user.password)  # パスワードをハッシュ化

        # superuser_flagをTrueに設定
        user.superuser_flag = True

        # 入力したパスワードをstart_passwordにも設定
        user.start_password = user.password  # ハッシュ化されたパスワードをstart_passwordにも設定
        
        # データベースに保存
        if commit:
            user.save()
        return user
    
# ユーザー登録
class UserSignUpForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ("account_id","company","password")
        labels = {'account_id':'ID', 'company':'企業名', 'password':'パスワード'}

    def save(self, commit=True):
        # ユーザーインスタンスを作成
        user = super().save(commit=False)
        
        # パスワードがハッシュ化されていなければハッシュ化
        if not user.password.startswith('pbkdf2_sha256$'):  # ハッシュ化されていない場合
            user.password = make_password(user.password)  # パスワードをハッシュ化

        # superuser_flagをTrueに設定
        user.superuser_flag = True

        # 入力したパスワードをstart_passwordにも設定
        user.start_password = user.password  # ハッシュ化されたパスワードをstart_passwordにも設定
        
        # データベースに保存
        if commit:
            user.save()
        return user
    
    
# ユーザーログイン
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = Users

# エラー報告画面
class ErrorReportForm(forms.ModelForm):
    class Meta:
        model = Error_report
        fields = ("id","error_detail","report_time")
        labels = {'id':'ID', 'error_detail':'報告内容','report_time':'日時'}

# ハラスメント報告画面
class HarassmentReportForm(forms.ModelForm):
    class Meta:
        model = Harassment_report
        fields = ("id","report_detail","report_image","report_time")
        labels = {'id':'ID', 'report_detail':'報告内容','report_image':'画像','report_time':'日時'}

        