from django.urls import path
from .views import signup_view, login_view,home_view,logout_view
from . import views

urlpatterns = [
    path('', home_view, name='home'),
    path("profile/",views.profile,name="profile"),
    path('signup/', signup_view, name='signup'),
    path('verify-otp-signup/', views.verify_otp_view_signup, name='verify-otp-signup'),
    path('login/', login_view, name='login'),
    path('login-with-otp/', views.request_otp_login, name='login_with_otp'),
    path('verify-otp-login/', views.verify_otp_login, name='verify_otp_login'),
    path('logout/', logout_view, name='logout_view'),
    path("send-otp/", views.send_otp_view, name="send_otp"),
    path("resend-otp/", views.resend_otp_view, name="resend_otp"),
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    path("reset-password/", views.reset_password_view, name="reset_password"),
    
]
