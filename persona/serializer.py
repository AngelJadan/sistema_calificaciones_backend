from django.forms import ChoiceField
from persona.models import Funcionario
from rest_framework import serializers
from django.contrib.auth.models import User


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
    password = serializers.CharField(help_text="Contraseña", max_length=128)
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
            "password",
        )

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
