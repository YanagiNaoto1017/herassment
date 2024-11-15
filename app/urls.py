from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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
    path('user_list', views.UserListView.as_view(), name='user_list'), # ユーザー一覧
    path('error_list', views.ErrorReportListView.as_view(), name='error_list'), # エラー一覧
    path('user_index/', views.UserIndexView.as_view(), name='user_index'), # ホーム画面
    path('detection/', views.DetectionView.as_view(), name='detection'), # 検出画面
    path('proofreading/', views.ProofreadingView.as_view(), name='proofreading'), # 検出画面
    path('user_signup/', views.UserSignupView.as_view(), name='user_signup'), # ユーザー登録
    path('harassment_report/', views.HarassmentReportView.as_view(), name='harassment_report'), #ハラスメント報告画面 
    path('error_report/', views.ErrorReportView.as_view(), name='error_report'), #エラー報告画面 
    path('check_id/', views.check_id, name='check_id'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('pw_send/', views.pw_send, name='pw_send'),
]