from django.contrib import admin
from django.urls import path
from . import views

app_name = "activity"

urlpatterns = [
    path("", views.activity_main, name="main"),
    path("user-rank/", views.user_rank, name="user_rank"),
    path("recycle-status/", views.recycle_log_status, name="recycle_status"),
    path("gallery/", views.gallery_view, name="gallery_view"),
    path("gallery/like_toggle/", views.like_toggle, name="like_toggle"),
]
