# Generated by Django 4.2 on 2024-11-29 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_harassment_report_report_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harassment_report',
            name='report_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/', verbose_name='画像'),
        ),
    ]