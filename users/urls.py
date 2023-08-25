from django.contrib import admin
from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("signup/", views.signup, name="signup"),
    path("mypage/", views.mypage_view, name="mypage_view"),
    path(
        "mypage/change_password",
        views.change_password_view,
        name="change_password_view",
    ),
]
