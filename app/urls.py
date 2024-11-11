from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='user_login'), # ユーザーログイン
    path('admin_login', views.LoginView.as_view(), name='admin_login'), # 管理者ログイン
    path('logout/', views.LogoutView.as_view(), name='logout'), # ログアウト
    path('admin_signup/', views.SignupView.as_view(), name='admin_signup'), # 管理者新規登録
    path('index/', views.IndexView.as_view(), name='index'), # ホーム画面
    path('company_signup', views.CompanySignupView.as_view(), name='company_signup'), # 企業登録
    path('superuser_signup', views.SuperUserSignupView.as_view(), name='superuser_signup'), # スーパーユーザー登録
    path('complete', views.CompleteView.as_view(), name='complete'), # 完了画面
    path('admin_list', views.AdminListView.as_view(), name='admin_list'), # 管理者一覧
    path('company_list', views.CompanyListView.as_view(), name='company_list'), # 企業一覧
]