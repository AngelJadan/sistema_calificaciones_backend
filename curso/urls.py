from django.contrib import admin
from django.urls import path, include
from curso import views

urlpatterns = [
    path("list-paralelos/", views.ListParalelos.as_view()),
    path("curso-api/", views.CursoAPI.as_view()),
    path("list-curso-all/", views.ListCursoAll.as_view()),
    path("list-area/", views.ListArea.as_view()),
    path("materia-api/", views.MateriaAPI.as_view()),
    path("list-materias/", views.ListMateria.as_view()),
    path("periodo-api/", views.PeriodoLectivoAPI.as_view()),
    path("list-periodo-all/", views.ListAllPeriodo.as_view()),
    path("last-periodo/", views.LastPeriodo.as_view()),
    path("materia-curso-docente-periodo/", views.MateriaCursoDocenteAPI.as_view()),
    path(
        "list-materia-curso-docente-periodo/", views.ListMateriaCursoDocente.as_view()
    ),
]
