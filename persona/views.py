from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from .serializer import UserSerializer


# Create your views here.
@api_view(["POST"])
@permission_classes([AllowAny])
def obtener_token(request):
    """
    Metodo para obtener el token e iniciar session.

    @username: Nombre del usuario.

    @password: Contraseña del usuario.

    @response: {'token': 'value'}: Respuesta exitosa con el token

    @response: 400: Respuesta de error.

    """
    username = request.data.get("username")
    password = request.data.get("password")

    if username and password:
        user = authenticate(username=username, password=password)

        if user:
            # Si el usuario es válido, se genera un nuevo token o se obtiene el existente
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Credenciales inválidas"}, status=400)
    else:
        return Response({"error": "Se requieren username y password"}, status=400)


class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
