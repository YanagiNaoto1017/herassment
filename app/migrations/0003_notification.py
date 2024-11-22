# Generated by Django 4.2 on 2024-11-22 04:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_users_account_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(default='', max_length=100, verbose_name='ユーザー名')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='送信日時')),
            ],
        ),
    ]
