from django.contrib import admin
from django.urls import path, include
from calificacion import views


urlpatterns = [
    path("materia-estudiante/", views.MateriaEstudianteAPI.as_view()),
    path("trimestre/", views.TrimestreEstudianteAPI.as_view()),
    path("list-curso-estudiante/<int:curso>/", views.ListEstudiantesCurso.as_view()),
    path(
        "list-materia-estudiante/<int:curso>/", views.ListEstudiantesMateria.as_view()
    ),
    path("list-periodo-curso/<int:periodo>/", views.ListPeriodoCurso.as_view()),
    path("cabecera-trimestre/", views.CabeceraTrimestreAPI.as_view()),
    path(
        "list-estudiante-cabecera-trimestre/<int:estudiante>/",
        views.ListEstudiantesCurso.as_view(),
    ),
    path("curso-materia/<int:curso_materia>/", views.api_view),
]
