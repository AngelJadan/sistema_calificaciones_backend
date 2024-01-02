from django.shortcuts import render
from persona.models import Funcionario
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema


from .serializer import (
    FuncionarioSerializer,
    FuncionarioSerializerExample,
    UserSerializer,
)

from django.contrib.auth.hashers import (
    make_password,
)


# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
def obtener_token(request):
    """
    Metodo para obtener el token e iniciar session.

    @email: Correo

    @password: Contraseña del usuario.

    @response: {'token': 'value'}: Respuesta exitosa con el token

    @response: 400: Respuesta de error.

    """
    email = request.data.get("email")
    password = request.data.get("password")

    if email and password:
        user = User.objects.get(email=email)
        user = authenticate(username=user.username, password=password)

        if user:
            # Si el usuario es válido, se genera un nuevo token o se obtiene el existente
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Credenciales inválidas"}, status=400)
    else:
        return Response({"error": "Se requieren username y password"}, status=400)


class Logout(APIView):
    """Clase api, para elimina el token y cerrar session."""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserListView(APIView):
    """ """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class FuncionarioUserView(generics.GenericAPIView):
    serializer_class = FuncionarioSerializerExample
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            pw = request.data["password"]
            pwd = make_password(pw)
            request.data["password"] = pwd
            serializer = FuncionarioSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, method="PUT")
    def put(self, request):
        try:
            id = request.POST.get("id")
            funcionario = Funcionario.objects.get(id=id)
            if request.user_is_authenticated:
                serializer = FuncionarioSerializer(
                    funcionario, data=request.data, context=request.context
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(
                    {"error": "Acceso no autorizado"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Funcionario.DoesNotExist:
            return Response(
                {"error": "No existe un funcionario con este id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="GET")
    def get(self, request):
        try:
            if request.user.is_authenticated:
                result = Funcionario.objects.get(id=request.query_params["id"])
                serializer = FuncionarioSerializer(data=result)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Acceso no autorizado"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Funcionario.DoesNotExist:
            return Response(
                {"error": "No existen datos con esta id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        try:
            if request.user.is_authenticated:
                if request.user.is_authenticated:
                    result = Funcionario.objects.get(
                        id=request.query_params["id"]
                    ).delete()
                    serializer = FuncionarioSerializer(data=result)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Acceso no autorizado"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        except Funcionario.DoesNotExist:
            return Response(
                {"error": "No existen datos con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
