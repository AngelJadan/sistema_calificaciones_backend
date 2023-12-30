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

    first_name = serializers.CharField(help_text="Primer nombre")
    last_name = serializers.CharField(help_text="Apellido")
    username = serializers.CharField(help_text="Nombre de usuario")
    email = serializers.EmailField(help_text="Correo electronico")


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = "__all__"
