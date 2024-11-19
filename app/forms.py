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
class AdminLoginForm(forms.Form):
    account_id = forms.CharField(
        max_length=150,
        required=True,
        label="管理者ID",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'account_id',
        })
    )
    password = forms.CharField(
        required=True,
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password',
        })
    )

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
class UserLoginForm(forms.Form):
    account_id = forms.CharField(
        max_length=150,
        required=True,
        label="ユーザーID",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'account_id',
        })
    )
    password = forms.CharField(
        required=True,
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password',
        })
    )

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

# ID確認
class CheckIdForm(forms.Form):
    account_id = forms.CharField(label='ユーザーID', max_length=100)

# メール送信
class SendEmailForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')

# スーパーユーザーへ送信
class SendSuperuserForm(forms.Form):
    superuser_name = forms.ChoiceField(
        choices=[(p['id'], p['id']) for p in Users.objects.values('id')],
        label="スーパーユーザー",
        required=True
    )
