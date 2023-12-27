from django.db import models

from persona.models import Funcionario


# Create your models here.
class Paralelo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Paralelo"
        verbose_name_plural = "Paralelos"


NIVEL = (
    ("1", "Educacion basica general"),
    ("2", "Bachiller"),
)


class Curso(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    nivel = models.CharField(max_length=5, choices=NIVEL, verbose_name="Nivel")
    paralelo = models.ForeignKey(
        Paralelo,
        related_name="paralelo_curso",
        on_delete=models.CASCADE,
        verbose_name="Paralelo",
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"


class Area(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"


class Materia(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    area = models.ForeignKey(
        Area, on_delete=models.CASCADE, related_name="area_materia", verbose_name="Area"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"


class MateriaCursoDocente(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    periodo = models.IntegerField(verbose_name="Periodo")
    periodo_abierto = models.BooleanField(verbose_name="Periodo abierto")
    inicio_periodo = models.DateField(verbose_name="Inicio periodo")
    cierre_periodo = models.DateField(verbose_name="Cierre periodo")
    curso = models.ForeignKey(
        Curso,
        related_name="curso_materia",
        on_delete=models.CASCADE,
        verbose_name="Curso",
    )
    materia = models.ForeignKey(
        Materia,
        related_name="materia",
        on_delete=models.CASCADE,
        verbose_name="Materia",
    )
    docente = models.ForeignKey(
        Funcionario,
        related_name="docente",
        on_delete=models.CASCADE,
        verbose_name="Funcionario",
    )

    def __str__(self):
        return f"{self.periodo}"

    class Meta:
        verbose_name = "Materia curso docente"
        verbose_name_plural = "Materias curso docente"
