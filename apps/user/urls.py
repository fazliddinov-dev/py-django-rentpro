from django.urls import path

from .views.otp_view import SendOTPView, VerifyOTPView
from .views.register_view import ListUser, RegisterView
from .views.super_admin_auth import SuperAdminLoginView

urlpatterns = [
    path("super-admin-login/", SuperAdminLoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("list-users/", ListUser.as_view()),
    path("send-otp/", SendOTPView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
]
