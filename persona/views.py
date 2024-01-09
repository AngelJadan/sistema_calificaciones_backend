from persona.models import Estudiante, Funcionario
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
from rest_framework.generics import UpdateAPIView, ListAPIView


from .serializer import (
    ChangePasswordSerializer,
    EstudianteSerializer,
    FuncionarioReadSerializer,
    FuncionarioSerializer,
    FuncionarioSerializerExample,
    UserSerializer,
)

from django.contrib.auth.hashers import (
    check_password,
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
    permission_classes = [AllowAny]

    def post(self, request):
        pw = request.data["password"]
        pwd = make_password(pw)
        request.data["password"] = pwd
        serializer = FuncionarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        try:
            print(f"request.POST.get('id') {request.data.get('id')}")
            id = request.data.get("id")
            funcionario = Funcionario.objects.get(id=id)

            if request.user.is_authenticated:
                serializer = FuncionarioReadSerializer(funcionario, data=request.data)
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
    def get(self, request, *args, **kwargs):
        """
        @query_params:
        @email: Correo de registro.
        """
        try:
            if request.user.is_authenticated:
                result = Funcionario.objects.get(email=request.query_params["email"])
                serializer = FuncionarioReadSerializer(result, many=False)
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


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Credenciales incorrectos"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"sms": "Contraseña actualizada."}, status=status.HTTP_200_OK
            )


class ListFuncionario(ListAPIView):
    serializer_class = FuncionarioReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            try:
                funcionario = Funcionario.objects.get(id=self.request.user.id)
                if funcionario.tipo != "1":
                    return Funcionario.objects.all()
                else:
                    return []
            except Funcionario.DoesNotExist:
                return []

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Verifica si la queryset está vacía (caso específico según tus necesidades)
        if not queryset:
            return Response(
                {"mensaje": "No tienes permiso para acceder a estos datos"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EstudianteUserView(generics.GenericAPIView):
    serializer_class = EstudianteSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        pw = "jkjklfjklj254545"
        pwd = make_password(pw)
        request.data["password"] = pwd
        serializer = EstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        try:
            id = request.data.get("id")
            estudiante = Estudiante.objects.get(id=id)

            if request.user.is_authenticated:
                serializer = EstudianteSerializer(estudiante, data=request.data)
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
    def get(self, request, *args, **kwargs):
        """
        @query_params:
        @id: Id de registro.
        """
        try:
            if request.user.is_authenticated:
                result = Estudiante.objects.get(id=request.query_params["id"])
                serializer = EstudianteSerializer(result, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Acceso no autorizado"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Estudiante.DoesNotExist:
            return Response(
                {"error": "No existen datos con esta id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        try:
            if request.user.is_authenticated:
                if request.user.is_authenticated:
                    result = Estudiante.objects.get(
                        id=request.query_params["id"]
                    ).delete()
                    serializer = EstudianteSerializer(data=result)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Acceso no autorizado"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
        except Estudiante.DoesNotExist:
            return Response(
                {"error": "No existen datos con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListEstudiante(ListAPIView):
    serializer_class = EstudianteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            try:
                funcionario = Funcionario.objects.get(id=self.request.user.id)
                if funcionario.tipo != "1":
                    return Estudiante.objects.all()
                else:
                    return []
            except Funcionario.DoesNotExist:
                return []

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Verifica si la queryset está vacía (caso específico según tus necesidades)
        if not queryset:
            return Response(
                {"mensaje": "No tienes permiso para acceder a estos datos"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
