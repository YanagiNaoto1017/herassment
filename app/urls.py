from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('admin_signup/', views.SignupView.as_view(), name='admin_signup'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('company_signup', views.CompanySignupView.as_view(), name='company_signup'),
    # path('superuser_signup', views.SuperUserSignupView.as_view(), name='superuser_signup'),
]