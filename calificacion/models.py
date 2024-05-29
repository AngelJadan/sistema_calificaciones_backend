from django.db import models
from curso.models import MateriaCursoDocente
from django.contrib.auth.models import User

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
    materia_curso = models.ForeignKey(
        MateriaCursoDocente,
        on_delete=models.CASCADE,
        related_name="materia_curso",
        verbose_name="Materia curso",
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Materia estudiante"
        verbose_name_plural = "Materia estudiantes"


CALIFICACION = (
    ("0", "(NE) No evaluado"),
    ("1", "(I) Destreza o aprendizaje iniciado"),
    ("2", "(EP) Destreza o aprendizaje en proceso de desarrollo"),
    ("3", "(A) Destreza o aprendizaje alcanzado"),
)


class CabeceraTrimestre(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    numero_trimestre = models.IntegerField(verbose_name="Numero trimestre")
    materia_estudiante = models.ForeignKey(
        MateriaEstudiante,
        on_delete=models.CASCADE,
        related_name="estudiante_trimestre",
        verbose_name="Materia estudiante",
    )
    aporte_cualitativo = models.CharField(
        max_length=1, choices=CALIFICACION, verbose_name="Aporte cualitativo"
    )
    proyecto_integrador = models.FloatField(verbose_name="Proyecto integrador")
    cualitativo_proyecto_integrador = models.CharField(
        max_length=1,
        choices=CALIFICACION,
        verbose_name="Cualitativo proyecto integrador",
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario",
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Cabecera trimestre"
        verbose_name_plural = "Cabecera trimestres"


TIPO_APORTE = (
    ("1", "Actividades Disciplinares o indisciplinares individiales"),
    ("2", "Actividades Disciplinares o indisciplinares grupales"),
)

ACTIVIDADES = (
    ("1", "Leccion"),
    ("2", "Prueba"),
    ("3", "Tarea"),
    ("4", "Proyecto"),
    ("5", "Exposicion"),
    ("6", "Taller"),
)


class Calificacion(models.Model):

    id = models.AutoField(primary_key=True, verbose_name="Id")
    aporte = models.CharField(choices=TIPO_APORTE, max_length=1, verbose_name="Aporte")
    actividad = models.CharField(
        choices=ACTIVIDADES, max_length=1, verbose_name="Actividad"
    )
    item = models.IntegerField(verbose_name="Item")
    calificacion = models.CharField(max_length=1, choices=CALIFICACION)
    trimestre = models.ForeignKey(
        CabeceraTrimestre,
        on_delete=models.CASCADE,
        related_name="calificacion_detalle",
        verbose_name="Detalle trimestre",
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Calificacion"
        verbose_name_plural = "Calificaciones"
