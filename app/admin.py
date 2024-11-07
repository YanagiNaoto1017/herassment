from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from .models import Admin

admin.site.register(Admin)  # Userモデルを登録
admin.site.unregister(Group)
