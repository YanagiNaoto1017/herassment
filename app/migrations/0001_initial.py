# Generated by Django 4.2 on 2025-01-28 02:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='企業ID')),
                ('company_name', models.CharField(max_length=50, unique=True, verbose_name='企業名')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
            ],
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100, verbose_name='単語')),
            ],
        ),
        migrations.CreateModel(
            name='Error_report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('inquiry_type', models.CharField(choices=[('type1', 'サービスについて'), ('type2', 'アカウント・ログインについて'), ('type3', '不具合について'), ('type4', '改善要望'), ('type5', 'その他')], default='type1', max_length=50, verbose_name='お問い合わせ種類')),
                ('error_detail', models.TextField(verbose_name='内容')),
                ('report_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='報告日時')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_name', models.CharField(max_length=50, null=True, verbose_name='送り元')),
                ('company_id', models.CharField(max_length=50, null=True, verbose_name='企業ID')),
                ('destination', models.CharField(max_length=50, null=True, verbose_name='送り先')),
                ('genre', models.CharField(max_length=50, null=True, verbose_name='通知種類')),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='送信日時')),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('input_text', models.TextField(verbose_name='入力文章')),
                ('harassment_flag', models.BooleanField(default=False, verbose_name='ハラスメントフラグ')),
                ('text_flag', models.BooleanField(default=False, verbose_name='テキストフラグ')),
                ('detected_words', models.CharField(max_length=100, null=True, verbose_name='検出単語')),
            ],
        ),
        migrations.CreateModel(
            name='Harassment_report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('report_title', models.CharField(default='', max_length=50, verbose_name='タイトル')),
                ('report_detail', models.TextField(verbose_name='内容')),
                ('report_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='報告日時')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.company', verbose_name='企業id')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('account_id', models.CharField(max_length=50, null=True, unique=True, verbose_name='ユーザーID')),
                ('account_name', models.CharField(default='', max_length=50, verbose_name='ユーザーネーム')),
                ('password', models.CharField(max_length=500, verbose_name='パスワード')),
                ('start_password', models.CharField(max_length=500, verbose_name='初期パスワード')),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='メールアドレス')),
                ('user_flag', models.BooleanField(default=False, verbose_name='ユーザーフラグ')),
                ('superuser_flag', models.BooleanField(default=False, verbose_name='スーパーユーザーフラグ')),
                ('admin_flag', models.BooleanField(default=False, verbose_name='管理者フラグ')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='is_superuser')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='登録日時')),
                ('update_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新日時')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.company', verbose_name='企業名')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
