from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Company,Users,Harassment_report,Error_report,Text
from django.contrib.auth.hashers import make_password

# 管理者新規登録
class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ("account_id","account_name","email",)

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
    
# ログイン
class LoginForm(AuthenticationForm):
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
        choices=[(p['account_name'], p['account_name']) for p in Users.objects.filter(superuser_flag=True).values('account_name')],
        label="誰に送りますか？",
        required=True
    )


#検出
class DetectionForm(forms.Form):
    input_text = forms.CharField(label='検出', max_length=500)

#パスワード変更
class CustomPasswordChangeForm(forms.Form):
    new_password = forms.CharField(
        label=("新しいパスワード"),
        max_length=500,
    )
    new_password2 = forms.CharField(
        label=("パスワードの確認"),
        max_length=500,
    )
        
class SearchForm(forms.Form):
    search_text = forms.CharField(required=False, label='名前', widget=forms.TextInput(attrs={'placeholder': '名前で検索'}))