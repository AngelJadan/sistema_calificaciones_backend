from django.contrib import admin
from django.urls import path, include

from persona.views import UserListView
from persona import views

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path(
        "funcionario-api/", views.FuncionarioUserView.as_view(), name="funcionario-api/"
    ),
    path("estudiante-api/", views.EstudianteUserView.as_view(), name="estudiante-api/"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path("list_funcionario/", views.ListFuncionario.as_view(), name="list_funcionario"),
    path("list_estudiante/", views.ListFuncionario.as_view(), name="list_estudiante"),
]
