from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Company,Users,Harassment_report,Error_report,Text
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import re
from django.core.validators import RegexValidator

# 管理者新規登録
class AdminSignUpForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ("account_id","account_name","email","password1","password2")

    def clean_account_id(self):
        account_id = self.cleaned_data.get('account_id')
        if re.search(r'[ぁ-んァ-ン一-龥]', account_id):
            raise ValidationError("アカウントIDに日本語を含めることはできません。")
        return account_id
    
    password1 = forms.CharField(
        label=("パスワード"),
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(attrs={'placeholder': '8〜16文字の半角英数字および記号を使用できます',}),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
    )

    password2 = forms.CharField(
        label=("パスワードの確認"),
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
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
        fields = ("account_id","account_name","company","email","password1","password2")

    def clean_account_id(self):
        account_id = self.cleaned_data.get('account_id')
        if re.search(r'[ぁ-んァ-ン一-龥]', account_id):
            raise ValidationError("アカウントIDに日本語を含めることはできません。")
        return account_id
    
    password1 = forms.CharField(
        label=("パスワード"),
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(attrs={'placeholder': '8〜16文字の半角英数字および記号を使用できます',}),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
    )

    password2 = forms.CharField(
        label=("パスワードの確認"),
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
    )
    
# ユーザー登録
class UserSignUpForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ("account_id","account_name","password1","password2")

    def clean_account_id(self):
        account_id = self.cleaned_data.get('account_id')
        if re.search(r'[ぁ-んァ-ン一-龥]', account_id):
            raise ValidationError("アカウントIDに日本語を含めることはできません。")
        return account_id
    
    password1 = forms.CharField(
        label=("パスワード"),
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(attrs={'placeholder': '8〜16文字の半角英数字および記号を使用できます',}),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
    )

    password2 = forms.CharField(
        label=("パスワードの確認"),
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
    )
    
# ログイン
class LoginForm(AuthenticationForm):
    class Meta:
        model = Users
    

# お問い合わせ画面
class ErrorReportForm(forms.ModelForm):
    class Meta:
        model = Error_report
        fields = ("id","inquiry_type","error_detail",)

# ハラスメント報告画面
class HarassmentReportForm(forms.ModelForm):
    class Meta:
        model = Harassment_report
        fields = ("id","report_title","report_detail","images")

    # 画像アップロード
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),  # ClearableFileInputを使用
        required=False,
        label="画像を追加"
    )

    report_title = forms.CharField(
        label=("タイトル"),
        max_length=100,
    )

    report_detail = forms.CharField(
        label=("内容"),
        max_length=500,
        widget=forms.Textarea(attrs={'placeholder': '報告内容を入力してください'},),
    )

# ID確認
class CheckIdForm(forms.Form):
    account_id = forms.CharField(label='ユーザーID', max_length=100)

# メール送信
class SendEmailForm(forms.Form):
    # email = forms.EmailField(label='メールアドレス', max_length=100)
    label = "登録の際に使用したメールアドレスにパスワード再設定用URLを記載したメールを送信しました" #これ表示されません　気にしないで


# スーパーユーザーへ送信
class SendSuperuserForm(forms.Form):
    superuser_name = forms.ChoiceField(
        choices=[(p['account_name'], p['account_name']) for p in Users.objects.filter(superuser_flag=True).values('account_name')],
        label="誰に送りますか？",
        required=True
    )


#検出
class DetectionForm(forms.Form):
    input_text = forms.CharField(
        label='検出',
        max_length=500,
        widget=forms.Textarea()
    )

#パスワード変更
class CustomPasswordChangeForm(forms.Form):
    new_password = forms.CharField(
        label=("新しいパスワード"),
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(attrs={'placeholder': '8〜16文字の半角英数字および記号を使用できます',}),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],

    )
    new_password2 = forms.CharField(
        label=("パスワードの確認"),
        min_length=8,
        max_length=16,
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
    )

# メールアドレス変更
class MailChangeForm(forms.Form):
    new_email = forms.EmailField(label='新しいメールアドレス')
        
class SearchForm(forms.Form):
    search_text = forms.CharField(required=False, initial='', widget=forms.TextInput(attrs={'type': 'text'}))
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    search_text = forms.CharField(required=False, label='名前', widget=forms.TextInput(attrs={'placeholder': '名前で検索'}))


#メールからのパスワード変更
class MailPWChangeForm(forms.Form):
    new_password = forms.CharField(
        label=("新しいパスワード"),
        min_length=8,
        max_length=500,
        widget=forms.PasswordInput(attrs={'placeholder': '8〜16文字の半角英数字および記号を使用できます',}),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
    )
    new_password2 = forms.CharField(
        label=("パスワードの確認"),
        min_length=8,
        max_length=500,
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex='^[a-zA-Z0-9!@#$%^&*()_+={}\[\]:;"\'<>?,./~`-]+$',
                message='パスワードは8〜16文字の半角英数字および記号で入力してください。',
            )
        ],
    )
