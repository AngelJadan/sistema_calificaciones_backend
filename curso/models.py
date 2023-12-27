from django.db import models


# Create your models here.
class Paralelo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Id")
    nombre = models.CharField(max_length="50", verbose_name="Nombre")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Paralelo"
        verbose_name_plural = "Paralelos"
