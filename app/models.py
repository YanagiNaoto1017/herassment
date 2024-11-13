from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
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

# 管理者
class Admin(AbstractBaseUser,PermissionsMixin):
    # Adminモデルに固有のrelated_nameを指定
    groups = models.ManyToManyField(Group, related_name='admin_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='admin_permissions')

    account_id = models.CharField(
        verbose_name=_("account_id"),
        unique=True,
        max_length=10,
        blank=True,
        null=True
    )
    email = models.EmailField(unique=True,max_length=255)
    password = models.CharField(max_length=255,null=True,blank=True)
    is_superuser = models.BooleanField(
        verbose_name=_("is_superuser"),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=True,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'account_id' # ログイン時、ユーザー名の代わりにaccount_idを使用
    REQUIRED_FIELDS = ['email']  # スーパーユーザー作成時にemailも設定する

    def __str__(self):
        return self.account_id

# 企業
class Company(models.Model):
    id = models.BigIntegerField(primary_key=True,null=False,blank=False,unique=True)
    company_name = models.CharField(max_length=50,null=False,blank=False,unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.company_name  # 企業名を返す

# ハラスメント報告
class Harassment_report(models.Model):
    id = models.AutoField(primary_key=True)
    report_detail = models.TextField(null=False) # 報告内容
    report_image = models.CharField(max_length=100,null=True)
    report_time = models.DateTimeField(default=timezone.now)

# エラー報告
class Error_report(models.Model):
    id = models.AutoField(primary_key=True)
    error_detail = models.TextField(null=False) # 報告内容
    report_time = models.DateTimeField(default=timezone.now)

# 文章
class Text(models.Model):
    id = models.AutoField(primary_key=True)
    input_text = models.TextField(null=False)
    harassment_flag = models.BooleanField(default=False)
    text_flag = models.BooleanField(default=False)
    detected_words = models.CharField(max_length=100,null=True)

# 辞書
class Dictionary(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=100,null=False) # 単語

# ユーザー
class Users(AbstractBaseUser,PermissionsMixin):
    # Usersモデルに固有のrelated_nameを指定
    groups = models.ManyToManyField(Group, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')

    account_id = models.CharField(
        verbose_name=_("account_id"),
        unique=True,
        max_length=10,
        blank=True,
        null=True
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE) # 企業ID
    password = models.CharField(max_length=50,null=False)
    start_password = models.CharField(max_length=50,null=False) # 初期パスワード
    email = models.EmailField(null=True)
    superuser_flag = models.BooleanField(default=False) # スーパーユーザーフラグ
    is_superuser = models.BooleanField(
        verbose_name=_("is_superuer"),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'account_id' # ログイン時、ユーザー名の代わりにaccount_idを使用
    REQUIRED_FIELDS = ['email']  # スーパーユーザー作成時にemailも設定する

    def __str__(self):
        return self.account_id