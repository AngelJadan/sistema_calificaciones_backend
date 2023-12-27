from django.contrib import admin

from persona.models import Estudiante, Funcionario, Persona

# Register your models here.


class PersonaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "identificacion",
        "tipo_identificacion",
    )


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("fecha_inicio", "fecha_final", "tipo")


class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("fecha_nacimiento",)


admin.site.register(Persona, PersonaAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
