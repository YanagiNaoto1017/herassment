from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
 
class UserManager(BaseUserManager):
    def _create_user(self, email, account_id, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, account_id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
 
        return user
 
    def create_user(self, email, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            account_id=account_id,
            password=password,
            **extra_fields,
        )
 
    def create_superuser(self, email, account_id, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            email=email,
            account_id=account_id,
            password=password,
            **extra_fields,
        )
 
# 企業
class Company(models.Model):
    id = models.BigIntegerField(verbose_name=_("企業ID"),primary_key=True,null=False,blank=False,unique=True)
    company_name = models.CharField(verbose_name=_("企業名"),max_length=50,null=False,blank=False,unique=True)
    created_at = models.DateTimeField(verbose_name=_("登録日時"),default=timezone.now)
 
    def __str__(self):
        return self.company_name  # 企業名を返す
 
# ハラスメント報告
class Harassment_report(models.Model):
    id = models.AutoField(verbose_name=_("ID"),primary_key=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        verbose_name=_("企業id"),
        null=True,
    )
    report_title = models.CharField(verbose_name=_("タイトル"),null=False,blank=False,max_length=50,default="",)
    report_detail = models.TextField(verbose_name=_("内容"),null=False)
    report_time = models.DateTimeField(verbose_name=_("報告日時"),default=timezone.now)

# 画像
class HarassmentReportImage(models.Model):
    report = models.ForeignKey(Harassment_report, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name=_("画像"),null=True,blank=True,upload_to='images/')
    uploaded_at = models.DateTimeField(verbose_name=_("アップロード日時"),default=timezone.now)

# エラー報告
# お問い合わせ
class Error_report(models.Model):
    id = models.AutoField(verbose_name=_("ID"),primary_key=True)
    # ドロップダウンの選択肢
    INQUIRY_TYPE_CHOICES = [
        ('type1', 'サービスについて'),
        ('type2', 'アカウント・ログインについて'),
        ('type3', '不具合について'),
        ('type4', '改善要望'),
        ('type5', 'その他'),
    ]
    inquiry_type = models.CharField(
        verbose_name=_("お問い合わせ種類"),
        max_length=50,
        null=False,
        blank=False,
        default='type1',
        choices=INQUIRY_TYPE_CHOICES,
    )
    error_detail = models.TextField(verbose_name=_("内容"),null=False)
    report_time = models.DateTimeField(verbose_name=_("報告日時"),default=timezone.now)
 
# 文章
class Text(models.Model):
    id = models.AutoField(verbose_name=_("ID"),primary_key=True)
    input_text = models.TextField(verbose_name=_("入力文章"),null=False)
    harassment_flag = models.BooleanField(verbose_name=_("ハラスメントフラグ"),default=False)
    text_flag = models.BooleanField(verbose_name=_("テキストフラグ"),default=False)
    detected_words = models.CharField(verbose_name=_("検出単語"),max_length=100,null=True)
 
# 辞書
class Dictionary(models.Model):
    id = models.AutoField(verbose_name=_("ID"),primary_key=True)
    keyword = models.CharField(verbose_name=_("単語"),max_length=100,null=False) # 単語
 
# ユーザー
class Users(AbstractBaseUser,PermissionsMixin):
 
    account_id = models.CharField(
        verbose_name=_("ユーザーID"),
        max_length=50,
        unique=True,
        null=True,
    )
    account_name = models.CharField(
        verbose_name=_("ユーザーネーム"),
        max_length=50,
        null=False,
        default="",
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE,
        verbose_name=_("企業名"),
        null=True,
    )
    password = models.CharField(
        verbose_name=_("パスワード"),
        max_length=500,
        null=False,
    )
    start_password = models.CharField(
        verbose_name=_("初期パスワード"),
        max_length=500,
        null=False,
    )
    email = models.EmailField(
        verbose_name=_("メールアドレス"),
        null=True,
        unique=True,
    )
    user_flag = models.BooleanField(
        verbose_name=_("ユーザーフラグ"),
        default=False,
    )
    superuser_flag = models.BooleanField(
        verbose_name=_("スーパーユーザーフラグ"),
        default=False,
    )
    admin_flag = models.BooleanField(
        verbose_name=_("管理者フラグ"),
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name=_("is_superuser"),
        default=False,
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("登録日時"),
        default=timezone.now,
    )
    update_at = models.DateTimeField(
        verbose_name=_("更新日時"),
        default=timezone.now,
    )
 
    objects = UserManager()
 
    USERNAME_FIELD = 'account_id' # ログイン時、ユーザー名の代わりにaccount_idを使用
    REQUIRED_FIELDS = ['email']  # スーパーユーザー作成時にemailも設定する
 
    def __str__(self):
        return self.account_id
   
# 通知
class Notification(models.Model):
    id = models.AutoField(verbose_name=_("ID"),primary_key=True)
    sender_name = models.CharField(
        verbose_name=_("送り元"),
        max_length=50,
        null=True,
    )
    company_id = models.CharField(
        verbose_name=_("企業ID"),
        max_length=50,
        null=True,
    )
    destination = models.CharField(
        verbose_name=_("送り先"),
        max_length=50,
        null=True,
    )
    genre = models.CharField(
        verbose_name=_("通知種類"),
        max_length=50,
        null=True,
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        verbose_name=_("送信日時"),
        default=timezone.now,
    )