# Generated by Django 4.2 on 2024-11-11 05:05

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
                ('id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('company_name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('keyword', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Error_report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('error_detail', models.TextField()),
                ('report_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Harassment_report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('report_detail', models.TextField()),
                ('report_image', models.CharField(max_length=100, null=True)),
                ('report_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('input_text', models.TextField()),
                ('harassment_flag', models.BooleanField(default=False)),
                ('text_flag', models.BooleanField(default=False)),
                ('detected_words', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('start_password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('superuser_flag', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('account_id', models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='account_id')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='is_superuer')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
