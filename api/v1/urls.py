from django.urls import path

from .views.auth_view import LoginView
from .views.super_admin_auth import SuperAdminLoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("super-admin-login/", SuperAdminLoginView.as_view()),
]
