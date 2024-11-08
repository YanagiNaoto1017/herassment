from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class Admin(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50,null=False)
    created_at = models.DateTimeField(default=timezone.now)

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
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    password = models.CharField(max_length=50,null=False)
    start_password = models.CharField(max_length=50,null=False)
    email = models.EmailField(null=True)
    superuser_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)