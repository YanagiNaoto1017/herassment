from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Company,Users,Harassment_report,Error_report,Text
from django.contrib.auth.hashers import make_password

# 管理者新規登録
class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ("account_id","account_name","email",)

# 管理者ログイン
class AdminLoginForm(AuthenticationForm):
    class Meta:
        model = Users

# 企業登録
class CompanySignUpForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("id","company_name",)

# スーパーユーザー登録
class SuperUserSignUpForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ("account_id","account_name","company","email")
    
# ユーザー登録
class UserSignUpForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ("account_id","account_name")
    
    
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

# ID確認
class CheckIdForm(forms.Form):
    account_id = forms.CharField(label='IDを入力してください', max_length=100)

# メール送信
class SendEmailForm(forms.Form):
    email = forms.EmailField(label='メールアドレスを入力してください')

# スーパーユーザーへ送信
class SendSuperuserForm(forms.Form):
    superuser_name = forms.ChoiceField(
        choices=[(p['account_id'], p['account_id']) for p in Users.objects.filter(superuser_flag=True).values('account_id')],
        label="誰に送りますか？",
        required=True
    )

#検出
class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['input_text']
        widgets = {
            'input_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
