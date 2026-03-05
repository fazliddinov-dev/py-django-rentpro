from django.urls import path

from .views.auth_view import LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
]
