from django.contrib import admin

from calificacion.models import (
    CabeceraTrimestre,
    MateriaEstudiante,
)

# Register your models here.


class MateriaEstudianteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "estudiante",
        "materia_curso",
    )


class CabeceraTrimestreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "numero_trimestre",
        "materia_estudiante",
        "aporte_cualitativo",
        "proyecto_integrador",
        "cualitativo_proyecto_integrador",
        "usuario",
    )


class DetalleTrimestreAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo_aporte", "cabecera_trimestre")


admin.site.register(MateriaEstudiante, MateriaEstudianteAdmin)
admin.site.register(CabeceraTrimestre, CabeceraTrimestreAdmin)
