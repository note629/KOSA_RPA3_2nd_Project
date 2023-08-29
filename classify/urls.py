from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from RecyclableProject import settings
from . import views

app_name = "classify"

urlpatterns = [
    path("", views.image_upload, name="image_upload"),
    path("result/", views.classify_yolo, name="classify_yolo"),
    path("result/upload/", views.upload_to_gallery, name="upload_to_gallery"),
]
