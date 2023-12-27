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
        related_name="materia_estudiante",
        verbose_name="Materia estudiante",
    )
    aporte_cualitativo = models.CharField(
        max_length=1, choices=CALIFICACION, verbose_name="Aporte cualitativo"
    )
    proyecto_integrador = models.FloatField(vebose_name="Proyecto integrador")
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


class DetalleTrimestre(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    tipo_aporte = models.CharField(
        max_length=1, choices=TIPO_APORTE, verbose_name="Tipo aporte"
    )
    cabecera_trimestre = models.ForeignKey(
        CabeceraTrimestre,
        on_delete=models.CASCADE,
        related_name="cabecera_trimestre",
        verbose_name="Cabecera trimestre",
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Detalle trimestre"
        verbose_name_plural = "Detalle trimestres"


TIPO_ACTIVIDAD = (
    ("1", "LECCIONES ORALES/ESCRITAS"),
    ("2", "PRUEBAS BASE ESTRUCTURADA"),
    ("3", "TAREAS/EJERCICIOS"),
    ("4", "PROYECTOS INTEGRADORES"),
    ("5", "EXPOSICIONES/FOROS"),
    ("6", "TALLERES"),
)


class CabeceraActividad(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre = models.CharField(
        max_length=1, choices=TIPO_ACTIVIDAD, verbose_name="Nombre"
    )
    detalle_trimestre = models.ForeignKey(
        DetalleTrimestre,
        on_delete=models.CASCADE,
        related_name="detalle_trimestre",
        verbose_name="Detalle trimestre",
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Cabecera actividad"
        verbose_name_plural = "Cabecera actividades"

    def validar_actividad_tipo_aporte(self):
        pass


NOMBRE_TAREA = (
    ("1", "LECCION ESCRITA DE LAS PARTES ORACION"),
    ("2", "CUALITATIVO"),
)


class DetalleActividad(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre = models.CharField(max_length=1, choices=NOMBRE_TAREA, verbose_name="Nombre")
    calificacion = models.IntegerField(verbose_name="Calificacion")
    cabecera_actividad = models.ForeignKey(
        CabeceraActividad,
        on_delete=models.CASCADE,
        related_name="cabecera_actividad",
        verbose_name="Cabecera actividad",
    )

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Detalle actividad"
        verbose_name_plural = "Detalle actividades"
