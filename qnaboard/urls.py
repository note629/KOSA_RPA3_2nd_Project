from django.contrib import admin
from django.urls import path, include

from qnaboard import views

app_name = "qnaboard"

## 현재 URL => http://127.0.0.1:8000/qnaboard
urlpatterns = [
    path("list/", views.qb_list, name="list"),
    path("read/<int:post_id>/", views.qb_read, name="read"),
    path("create/", views.qb_create, name="create"),
    path("update/<int:post_id>/", views.qb_update, name="update"),
    path("delete/<int:post_id>/", views.qb_delete, name="delete"),
]
