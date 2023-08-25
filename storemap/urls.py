from django.contrib import admin
from django.urls import path
from storemap import views

app_name = "storemap"

urlpatterns = [
    path("", views.storemap_view, name="storemap_view"),
]
