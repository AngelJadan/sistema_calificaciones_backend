from django.forms import ChoiceField
from persona.models import Estudiante, Funcionario
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import (
    make_password,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class FuncionarioSerializerExample(serializers.Serializer):
    """
    Descripcion de la clase FuncionarioSerializer
    """

    TIPOS = ("1", "Docente")

    first_name = serializers.CharField(help_text="Primer nombre", max_length=150)
    last_name = serializers.CharField(help_text="Apellido", max_length=150)
    username = serializers.CharField(help_text="Nombre de usuario", max_length=150)
    email = serializers.EmailField(help_text="Correo electronico", max_length=254)
    fecha_ingreso = serializers.DateTimeField(
        help_text="Fecha de ingreso del funcionario",
    )
    fecha_salida = serializers.DateTimeField(
        help_text="Fecha de salida del funcionario"
    )
    tipo = serializers.CharField(
        help_text="Tipo: (1, Docente), (2, Rector), (3, Secretaria)",
    )
    identificacion = serializers.CharField(help_text="Numero de cedula", max_length=20)
    tipo_identificacion = serializers.CharField(help_text="1: Cedula, 2: Pasaporte")


class FuncionarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Funcionario
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "fecha_ingreso",
            "fecha_salida",
            "tipo",
            "identificacion",
            "tipo_identificacion",
        )

    def create(self, validated_data):
        password = Funcionario.generar_password()
        pw = password
        pwd = make_password(pw)
        new_password = pwd
        new_funcionario = Funcionario.objects.create(
            **validated_data,
            password=new_password,
        )
        # Pendiente implementar enviar password al correo.
        return new_funcionario

    def update(self, Funcionario, validated_data):
        return super().update(Funcionario, validated_data)


class FuncionarioReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "fecha_ingreso",
            "fecha_salida",
            "tipo",
            "identificacion",
            "tipo_identificacion",
        )


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante

        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "identificacion",
            "tipo_identificacion",
            "fecha_nacimiento",
        )

    def create(self, validated_data):
        password = Funcionario.generar_password()
        pw = password
        pwd = make_password(pw)
        new_password = pwd
        new_estudiante = Estudiante.objects.create(
            **validated_data,
            password=new_password,
        )
        # Pendiente implementar enviar password al correo.
        return new_estudiante

    def update(self, Estudiante, validated_data):
        return super().update(Estudiante, validated_data)
