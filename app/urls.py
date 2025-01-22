from django.urls import path
from . import views
from django.conf.urls import handler403, handler404, handler500
from .views import custom_403_view, custom_404_view, custom_500_view

app_name = 'app'

handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view

urlpatterns = [
    # ログイン関連
    path('', views.LoginView.as_view(), name='login'), # ログイン
    path('logout/', views.LogoutView.as_view(), name='logout'), # ログアウト
    path('check_id/', views.CheckIdView.as_view(), name='check_id'), # ID確認
    path('send_email/', views.SendEmailView.as_view(), name='send_email'), # メール送信
    path('send_superuser/', views.SendSuperuserView.as_view(), name='send_superuser'), # パスワードリセット要請

    # メール関連
    path('mail/password_change/', views.MailPWChangeView.as_view(), name='mail_PWchange'), #パスワード変更画面
    path('mail/password_complete/', views.MailPwCompleteView.as_view(), name='mail_PWcomp'), #パスワード再設定完了画面

    # 共通
    path('index/', views.IndexView.as_view(), name='index'), # ホーム画面

    # 管理者、スーパーユーザー
    path('user_list/', views.UserListView.as_view(), name='user_list'), # ユーザー一覧

    # 管理者のみ
    path('admin_signup/', views.SignupView.as_view(), name='admin_signup'), # 管理者新規登録
    path('company_signup/', views.CompanySignupView.as_view(), name='company_signup'), # 企業登録
    path('superuser_signup/', views.SuperUserSignupView.as_view(), name='superuser_signup'), # スーパーユーザー登録
    path('admin_list/', views.AdminListView.as_view(), name='admin_list'), # 管理者一覧
    path('company_list/', views.CompanyListView.as_view(), name='company_list'), # 企業一覧
    path('error_list/', views.ErrorReportListView.as_view(), name='error_list'), # エラー一覧
    path('admin_delete/<int:pk>/', views.AdminDeleteView.as_view(), name='admin_delete'), # 管理者削除
    path('superuser_delete/<str:sender_name>/', views.SuperuserDeleteView.as_view(), name='superuser_delete'), # スーパーユーザー削除

    # 完了画面
    path('signup/complete/', views.CompleteView.as_view(), name='complete'), # 登録完了画面
    path('report/complete/', views.ReportCompleteView.as_view(), name='report_complete'), # 報告完了画面
    path('delete/complete/', views.DeleteCompleteView.as_view(), name='delete_complete'), # 削除完了画面
    path('password_send/complete/', views.PwSendCompleteView.as_view(), name='pw_send_comp'), # メール送信完了画面
    path('password_change/complete/', views.PwChangeCompleteView.as_view(), name='pw_change_complete'), # PWリセット完了画面
    path('email_change/complete/', views.EmailChangeCompleteView.as_view(), name='email_change_comp'), # メールアドレス変更完了画面
    
    # ユーザーのみ
    path('user/detection/', views.DetectionView.as_view(), name='detection'), # 検出画面
    path('user/user_signup/', views.UserSignupView.as_view(), name='user_sigunp'), # ユーザー登録
    path('user/harassment_report/', views.HarassmentReportView.as_view(), name='harassment_report'), #ハラスメント報告画面 
    path('user/harassment_list/', views.HarassmentReportListView.as_view(), name='harassment_list'), # ハラスメント一覧
    path('user/harassment_detail/<int:pk>/', views.HarassmentDetailView.as_view(), name='harassment_detail'), # ハラスメント詳細画面
    path('user/error_report/', views.ErrorReportView.as_view(), name='error_report'), #エラー報告画面 
    path('user/account_info/', views.AccountInfoView.as_view(), name='account_info'), #アカウント情報確認画面
    path('user/password_change/', views.PasswordChangeView.as_view(), name='password_change'), #パスワード変更画面
    path('user/email_change/', views.EmailChangeView.as_view(), name='email_change'), #メールアドレス変更画面
    path('user/notification', views.NotificationView.as_view(), name='notification'), #PWリセット通知
    path('user/user_delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'), # ユーザー削除
    path('user/company_delete/<int:pk>/', views.CompanyDeleteView.as_view(), name='company_delete'), # 企業削除
    path('user/password_reset<str:sender_name>/', views.PasswordReset.as_view(), name='password_reset'), # パスワードリセット
    path('user/superuser_delete<int:pk>/', views.SendSuperuserDeleteView.as_view(), name='send_superuser_delete'), # スーパーユーザー削除要請
 ]