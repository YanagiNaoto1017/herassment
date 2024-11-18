from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Admin,Company,Users,Harassment_report,Error_report
from django.contrib.auth.hashers import make_password

# 管理者新規登録
class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ("account_id","email",)

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

# 管理者ログイン
class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = Admin

# 企業登録
class CompanySignUpForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("id","company_name",)

# スーパーユーザー登録
class SuperUserSignUpForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ("account_id","company","email")

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

# ハラスメント報告画面
class HarassmentReportForm(forms.ModelForm):
    class Meta:
        model = Harassment_report
        fields = ("id","report_detail","report_image","report_time")