from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from .models import Users

admin.site.register(Users)  # Userモデルを登録
admin.site.unregister(Group)
