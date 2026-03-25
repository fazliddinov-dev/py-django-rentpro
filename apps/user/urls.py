from django.urls import path
from .views.register_view import RegisterView, ListUser


urlpatterns = [
    # path("super-admin-login/", SuperAdminLoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("list-users/", ListUser.as_view()),
]
