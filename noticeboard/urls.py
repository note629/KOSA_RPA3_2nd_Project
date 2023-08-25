from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from noticeboard import views

app_name = "noticeboard"

## 현재 URL => http://127.0.0.1:8000/noticeboard
urlpatterns = [
    path("list/", views.nb_list, name="list"),
    path("read/<int:notice_id>/", views.nb_read, name="read"),
    path("create/", views.nb_create, name="create"),
    path("update/<int:notice_id>/", views.nb_update, name="update"),
    path("delete/<int:notice_id>/", views.nb_delete, name="delete"),
]
