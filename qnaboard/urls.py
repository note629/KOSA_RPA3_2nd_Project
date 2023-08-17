from django.contrib import admin
from django.urls import path, include

from qnaboard import views

app_name = "qnaboard"

## 현재 URL => http://127.0.0.1:8000/qnaboard
urlpatterns = [
    path("list/", views.p_list, name="list"),
    path("create/", views.p_create, name="create"),
]
