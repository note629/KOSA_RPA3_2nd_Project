from django.contrib import admin
from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login_view"),
    path("signup/", views.signup, name="signup"),
]
