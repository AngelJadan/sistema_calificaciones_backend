from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
TIPO_IDENTIFICACION = (
    ("1", "cedula"),
    ("2", "pasaporte"),
)


class Persona(User):
    identificacion = models.CharField(
        max_length=20, unique=True, verbose_name="Identificacion"
    )
    tipo_identificacion = models.CharField(
        max_length=2,
        choices=TIPO_IDENTIFICACION,
        verbose_name="Tipo identificacion",
    )

    def __str__(self):
        return self.identificacion

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def is_funcionario(self):
        user_type = None
        if Funcionario.objects.filter(id=self.id).count() > 0:
            return True
        else:
            False

    def is_estudiante(self):
        user_type = None
        if Estudiante.objects.filter(id=self.id).count() > 0:
            return True
        else:
            False


TIPO_FUNCIONARIO = (
    ("1", "Docente"),
    ("2", "Rector"),
    ("3", "Secretaria"),
)


class Funcionario(Persona):
    fecha_ingreso = models.DateField(verbose_name="Fecha inicio")
    fecha_salida = models.DateField(null=True, blank=True, verbose_name="Fecha final")
    tipo = models.CharField(max_length=2, choices=TIPO_FUNCIONARIO, verbose_name="Tipo")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Funcionario"
        verbose_name_plural = "Funcionarios"

    def generar_password():
        """Genera un string aleatorio de 10 dígitos con letras y números."""
        letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numeros = "0123456789"
        caracteres = letras + numeros
        return "".join(random.choice(caracteres) for _ in range(10))


class Estudiante(Persona):
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
