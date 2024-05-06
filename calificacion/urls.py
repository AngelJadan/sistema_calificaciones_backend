from django.contrib import admin
from django.urls import path, include
from calificacion import views


urlpatterns = [
    path("materia-estudiante/", views.MateriaEstudianteAPI.as_view()),
    path("list-materia-estudiante/<int:curso>/", views.ListEstudiantesCurso.as_view()),
]
