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

class Admin(AbstractBaseUser,PermissionsMixin):
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

class Company(models.Model):
    id = models.BigIntegerField(primary_key=True,null=False,blank=False,unique=True)
    company_name = models.CharField(max_length=50,null=False,blank=False,unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.company_name  # 企業名を返す

class Harassment_report(models.Model):
    id = models.AutoField(primary_key=True)
    report_detail = models.TextField(null=False)
    report_image = models.CharField(max_length=100,null=True)
    report_time = models.DateTimeField(default=timezone.now)

class Error_report(models.Model):
    id = models.AutoField(primary_key=True)
    error_detail = models.TextField(null=False)
    report_time = models.DateTimeField(default=timezone.now)

class Text(models.Model):
    id = models.AutoField(primary_key=True)
    input_text = models.TextField(null=False)
    harassment_flag = models.BooleanField(default=False)
    text_flag = models.BooleanField(default=False)
    detected_words = models.CharField(max_length=100,null=True)

class Dictionary(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=100,null=False)

class Users(models.Model):
    id = models.BigIntegerField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    password = models.CharField(max_length=50,null=False)
    start_password = models.CharField(max_length=50,null=False)
    email = models.EmailField(null=True)
    superuser_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)