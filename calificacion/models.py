from django.db import models

from persona.models import Estudiante

# Create your models here.


class MateriaEstudiante(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        related_name="estudiante_materia",
        verbose_name="Estudiante",
    )
