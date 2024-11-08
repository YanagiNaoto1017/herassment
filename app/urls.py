from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('admin_signup/', views.SignupView.as_view(), name='admin_signup'),
    path('admin_list/', views.ListView.as_view(), name='admin_list'),
]