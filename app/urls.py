from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('admin/login/', views.LoginView.as_view(), name='login'),
    path('admin/signup/', views.SignupView.as_view(), name='admin_signup'),
    path('admin/adminlist/', views.ListView.as_view(), name='admin_list'),
]