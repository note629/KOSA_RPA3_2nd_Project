from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from noticeboard import views

app_name = "noticeboard"

## 현재 URL => http://127.0.0.1:8000/noticeboard
urlpatterns = [
    path("notices/", views.nb_list, name="notice_list"),
    path("notices/<int:notice_id>/", views.nb_read, name="notice_read"),
]
