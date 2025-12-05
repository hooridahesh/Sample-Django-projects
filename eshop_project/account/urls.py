from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerView.as_view(), name='register_page'),
    path('login/', views.loginView.as_view(), name='login_page'),
    path('logout/', views.logoutView.as_view(), name='logout_page'),
    path('activate_account/<str:email_active_code>', views.activateAccountView.as_view(), name='activate_account'),
    path('forget_pass', views.forgetPasswordView.as_view(), name='forget_pass'),
    path('reset_pass/<active_code>', views.resetPasswordView.as_view(), name='reset_pass')
]
