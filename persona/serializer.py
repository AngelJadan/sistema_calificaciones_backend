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

    first_name = serializers.CharField(help_text="Primer nombre")
    last_name = serializers.CharField(help_text="Apellido")
    username = serializers.CharField(help_text="Nombre de usuario")
    email = serializers.EmailField(help_text="Correo electronico")
    fecha_ingreso = serializers.DateTimeField(
        help_text="Fecha de ingreso del funcionario"
    )
    fecha_salida = serializers.DateTimeField(
        help_text="Fecha de salida del funcionario"
    )
    tipo = serializers.CharField(
        help_text="Tipo: (1, Docente), (2, Rector), (3, Secretaria)"
    )
    password = serializers.CharField(help_text="Contraseña")
    identificacion = serializers.CharField(help_text="Numero de cedula")
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

    """
    def create(self, validated_data):
        print(f"validated_data {validated_data}")
        pw = validated_data.get("password")
        print(f"pw {pw}")
        funcionario = Funcionario(
            is_active=True,
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("first_name"),
            username=validated_data.get("username"),
            email=validated_data.get("email"),
            password=User(password=pw).set_password(pw),
            identificacion=validated_data.get("identificacion"),
            tipo_identificacion=validated_data.get("tipo_identificacion"),
            fecha_ingreso=validated_data.get("fecha_ingreso"),
            fecha_salida=validated_data.get("fecha_salida"),
            tipo=validated_data.get("tipo"),
        )
        funcionario.save()
        return funcionario
        """
