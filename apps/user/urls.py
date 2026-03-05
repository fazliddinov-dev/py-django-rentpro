from django.urls import path

from apps.user.views.super_admin_auth import SuperAdminLoginView

urlpatterns = [
    path("super-admin-login/", SuperAdminLoginView.as_view()),
]
