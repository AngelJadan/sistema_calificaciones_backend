from django.db import models


# Create your models here.
TIPO_IDENTIFICACION = (
    ("1", "cedula"),
    ("2", "pasaporte"),
)


class Persona(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    identificacion = models.CharField(max_length=20, verbose_name="Identificacion")
    tipo_identificacion = models.CharField(
        max_length=2, choices=TIPO_IDENTIFICACION, verbose_name="Tipo identificacion"
    )

    def __str__(self):
        return self.identificacion

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"


TIPO_FUNCIONARIO = (
    ("1", "Docente"),
    ("2", "Rector"),
    ("3", "Secretaria"),
)


class Rector(Persona):
    fecha_inicio = models.DateField(verbose_name="Fecha inicio")
    fecha_final = models.DateField(verbose_name="Fecha final")
    tipo = models.CharField(max_length=2, choices=TIPO_FUNCIONARIO, verbose_name="Tipo")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Rector"
        verbose_name_plural = "Rectores"


class Estudiante(Persona):
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
