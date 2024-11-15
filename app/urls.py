from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='user_login'), # ユーザーログイン
    path('admin/login', views.LoginView.as_view(), name='admin_login'), # 管理者ログイン
    path('logout/', views.LogoutView.as_view(), name='logout'), # ログアウト

    # 管理者とユーザー
    path('index/', views.IndexView.as_view(), name='index'), # ホーム画面
    path('user_list', views.UserListView.as_view(), name='user_list'), # ユーザー一覧

    # 管理者
    path('admin/signup/', views.SignupView.as_view(), name='admin_signup'), # 管理者新規登録
    path('admin/company_signup', views.CompanySignupView.as_view(), name='company_signup'), # 企業登録
    path('admin/superuser_signup', views.SuperUserSignupView.as_view(), name='superuser_signup'), # スーパーユーザー登録
    path('admin/admin_list', views.AdminListView.as_view(), name='admin_list'), # 管理者一覧
    path('admin/company_list', views.CompanyListView.as_view(), name='company_list'), # 企業一覧
    path('admin/error_list', views.ErrorReportListView.as_view(), name='error_list'), # エラー一覧

    # 完了画面
    path('complete', views.CompleteView.as_view(), name='complete'), # 登録完了画面
    path('report_complete', views.ReportCompleteView.as_view(), name='report_complete'), # 報告完了画面
    path('delete_complete', views.DeleteCompleteView.as_view(), name='delete_complete'), # 削除完了画面
    
    # ユーザー
    path('user/detection/', views.DetectionView.as_view(), name='detection'), # 検出画面
    path('userproofreading/', views.ProofreadingView.as_view(), name='proofreading'), # 検出画面
    path('user/user_signup/', views.UserSignupView.as_view(), name='user_signup'), # ユーザー登録
    path('user/harassment_report/', views.HarassmentReportView.as_view(), name='harassment_report'), #ハラスメント報告画面 
    path('user/error_report/', views.ErrorReportView.as_view(), name='error_report'), #エラー報告画面 
]