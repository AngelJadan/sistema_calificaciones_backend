from django.contrib import admin

from curso.models import Area, Curso, Materia, MateriaCursoDocente, Paralelo

# Register your models here.


class ParaleloAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")


class CursoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "nivel",
        "paralelo",
    )


class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")


class MateriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "area")


class MateriaCursoDocenteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "periodo",
        "periodo_abierto",
        "inicio_periodo",
        "cierre_periodo",
        "curso",
    )


admin.site.register(Paralelo, ParaleloAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(MateriaCursoDocente, MateriaCursoDocenteAdmin)
