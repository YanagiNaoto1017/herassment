from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Admin,Company,Users

# 管理者新規登録
class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ("account_id","email",)

# 管理者ログイン
class AdminLoginFrom(AuthenticationForm):
    class Meta:
        model = Admin

# 企業登録
class CompanySignUpForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("id","company_name",)
        labels = {'id':'企業ID', 'company_name':'企業名'}

# スーパーユーザー登録
class SuperUserSignUpForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ("id","company","email","password")
        labels = {'id':'ID', 'company':'企業名','email':'メールアドレス', 'password':'パスワード'}

    def save(self, commit=True):
        user = super().save(commit=False)  # インスタンスはまだ保存しない
        user.superuser_flag = True         # superuser_flagをTrueに設定
        if commit:
            user.save()                    # データベースに保存
        return user