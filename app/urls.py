from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('admin_signup/', views.SignupView.as_view(), name='admin_signup'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]