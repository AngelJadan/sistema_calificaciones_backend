from persona.models import Estudiante, Funcionario, Persona
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
from django.db.models import Q

from .serializer import (
    ChangePasswordSerializer,
    EstudianteSerializer,
    FuncionarioReadSerializer,
    FuncionarioSerializer,
    FuncionarioSerializerExample,
    UserSerializer,
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

    try:
        if email and password:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)

            if user:
                # Si el usuario es válido, se genera un nuevo token o se obtiene el existente
                token, created = Token.objects.get_or_create(user=user)

                tipo_user = "0"
                persona = Persona.objects.get(id=user.pk)

                if persona.is_funcionario:
                    funcionario = Funcionario.objects.get(id=persona.id)
                    tipo_user = funcionario.tipo

                return Response(
                    {
                        "id": persona.id,
                        "first_name": persona.first_name,
                        "last_name": persona.last_name,
                        "identification": persona.identificacion,
                        "type_identification": persona.tipo_identificacion,
                        "email": persona.email,
                        "type_user": tipo_user,
                        "token": token.key,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response({"error": "Credenciales inválidas"}, status=400)
        else:
            return Response({"error": "Se requieren username y password"}, status=400)
    except User.DoesNotExist:
        return Response({"error": "No existe el usuario."})
    except BaseException as ex:
        return Response({"error": ex}, status=500)


class Logout(APIView):
    """Clase api, para elimina el token y cerrar session."""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserListView(APIView):
    """"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class FuncionarioUserView(generics.GenericAPIView):
    serializer_class = FuncionarioSerializerExample
    permission_classes = [AllowAny]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = FuncionarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        try:
            id = request.data.get("id")
            funcionario = Funcionario.objects.get(id=id)
            if request.user.is_authenticated:
                serializer = FuncionarioSerializer(funcionario, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
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
                id_recibed = request.query_params["id"]
                if request.user != User.objects.get(id=id_recibed):
                    Funcionario.objects.get(id=id_recibed).delete()
                    return Response(
                        {"sms": "Funcionaro eliminado."}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"error": "No se puede eliminar este usuario, autentificado."}
                    )
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
                    return Funcionario.objects.filter(~Q(id=self.request.user.id))
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
        serializer = EstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        try:
            id = request.data["id"]
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
        except Estudiante.DoesNotExist:
            return Response(
                {"error": "No existe un estudiante con este id."},
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
                    return Response(
                        {"sms": "Estudiante eliminado"}, status=status.HTTP_200_OK
                    )
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
            return Estudiante.objects.all()

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
