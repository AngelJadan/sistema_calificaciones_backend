from django.contrib import admin
from django.urls import path, include

from persona.views import UserListView
from persona import views

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("obtener_token/", views.obtener_token, name="obtener_token"),
]
