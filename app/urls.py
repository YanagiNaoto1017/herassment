from django.urls import path
from . import views
from django.conf.urls import handler403, handler404, handler500
from app.views import Custom403View, Custom404View, Custom500View

app_name = 'app'

handler403 = Custom403View.as_view()
handler404 = Custom404View.as_view()
handler500 = Custom500View.as_view()

urlpatterns = [
    path('accounts/login/', views.UserLoginView.as_view(), name='user_login'),  # ユーザーログイン
    path('', views.UserLoginView.as_view(), name='user_login'), # ユーザーログイン
    path('login', views.AdminLoginView.as_view(), name='admin_login'), # 管理者ログイン
    path('logout/', views.LogoutView.as_view(), name='logout'), # ログアウト
    path('check_id/', views.CheckIdView.as_view(), name='check_id'), # ID確認
    path('forget_password/', views.ForgetPasswordView.as_view(), name='forget_password'), # メール送信

    # 管理者とユーザー
    path('index/', views.IndexView.as_view(), name='index'), # ホーム画面
    path('user_list', views.UserListView.as_view(), name='user_list'), # ユーザー一覧

    # 管理者
    path('admin_signup/', views.SignupView.as_view(), name='admin_signup'), # 管理者新規登録
    path('company_signup', views.CompanySignupView.as_view(), name='company_signup'), # 企業登録
    path('superuser_signup', views.SuperUserSignupView.as_view(), name='superuser_signup'), # スーパーユーザー登録
    path('admin_list', views.AdminListView.as_view(), name='admin_list'), # 管理者一覧
    path('company_list', views.CompanyListView.as_view(), name='company_list'), # 企業一覧
    path('error_list', views.ErrorReportListView.as_view(), name='error_list'), # エラー一覧
    path('admin_delete/<int:pk>/', views.AdminDeleteView.as_view(), name='admin_delete'), # 管理者削除

    # 完了画面
    path('complete', views.CompleteView.as_view(), name='complete'), # 登録完了画面
    path('report_complete', views.ReportCompleteView.as_view(), name='report_complete'), # 報告完了画面
    path('delete_complete', views.DeleteCompleteView.as_view(), name='delete_complete'), # 削除完了画面
    path('pw_send_comp', views.PwSendCompleteView.as_view(), name='pw_send_comp'), # メール送信完了画面
    
    # ユーザー
    path('user/detection/', views.DetectionView.as_view(), name='detection'), # 検出画面
    path('userproofreading/', views.ProofreadingView.as_view(), name='proofreading'), # 検出画面
    path('user/user_signup/', views.UserSignupView.as_view(), name='user_sigunp'), # ユーザー登録
    path('user/harassment_report/', views.HarassmentReportView.as_view(), name='harassment_report'), #ハラスメント報告画面 
    path('usr/harassment_list', views.HarassmentReportListView.as_view(), name='harassment_list'), # ハラスメント一覧
    path('user/error_report/', views.ErrorReportView.as_view(), name='error_report'), #エラー報告画面 
    path('user/account_info/', views.AccountInfoView.as_view(), name='account_info'), #アカウント情報確認画面
    path('user/password_change/', views.PasswordChangeView.as_view(), name='password_change'), #パスワード変更画面
    path('user/notification', views.NotificationView.as_view(), name='notification'), #PWリセット通知
    path('user/user_delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete') # ユーザー削除
    path('user/reset_password<int:pk>/', views.PasswordReset.as_view(), name='password_reset') # パスぱーど
    ]