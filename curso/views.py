from calificacion.models import MateriaEstudiante
from curso.models import (
    Area,
    Curso,
    PeriodoLectivo,
    Materia,
    MateriaCursoDocente,
    Paralelo,
)
from curso.serializer import (
    AreaSerializer,
    CursoSerializer,
    CursoSerializerRead,
    MateriaCursoDocenteReadSerializer,
    MateriaCursoDocenteSerializer,
    MateriaEstudianteSerializer,
    MateriaReadSerializer,
    MateriaSerializer,
    ParaleloReadSerializer,
    PeriodoLectivoSerializer,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import action


# Create your views here.


class ListParalelos(ListAPIView):
    serializer_class = ParaleloReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Paralelo.objects.all()
        else:
            return []


class ListCursoAll(ListAPIView):
    """
    Api para listar los cursos,
    """

    serializer_class = CursoSerializerRead
    permissio_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Curso.objects.all()
        else:
            return []


class CursoAPI(generics.GenericAPIView):
    serializer_class = CursoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = CursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            curso = Curso.objects.get(id=id)
            serializer = CursoSerializer(curso, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Curso.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="GET")
    def get(self, request, *args, **kwargs):
        """
        @queryparam: id
        """
        try:
            result = Curso.objects.get(id=request.query_params.get("id"))
            serializer = CursoSerializer(result, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Curso.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        """
        @queryparam: id
        """
        try:
            result = Curso.objects.filter(id=request.query_params.get("id")).delete()
            return Response(
                {"sms": "Curso eliminado satisfactoriamente."},
                status=status.HTTP_200_OK,
            )
        except Curso.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AreaAPI(generics.GenericAPIView):
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = CursoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            curso = Curso.objects.get(id=id)
            serializer = CursoSerializer(curso, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Curso.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="GET")
    def get(self, request, *args, **kwargs):
        """
        @queryparam: id
        """
        try:
            result = Curso.objects.get(id=request.query_params.get("id"))
            serializer = CursoSerializer(result, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Curso.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        """
        @queryparam: id
        """
        try:
            result = Curso.objects.filter(id=request.query_params.get("id")).delete()
            return Response(
                {"sms": "Curso eliminado satisfactoriamente."},
                status=status.HTTP_200_OK,
            )
        except Curso.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListArea(ListAPIView):
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Area.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Verifica si la queryset está vacía (caso específico según tus necesidades)
        if not self.request.user.is_authenticated:
            return Response(
                {"mensaje": "No tienes permiso para acceder a estos datos"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MateriaAPI(generics.GenericAPIView):
    serializer_class = MateriaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = MateriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            curso = Materia.objects.get(id=id)
            serializer = MateriaSerializer(curso, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Materia.DoesNotExist:
            return Response(
                {"error": "No existe una materia con este id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="GET")
    def get(self, request, *args, **kwargs):
        """
        @queryparam: id
        """
        try:
            result = Materia.objects.get(id=request.query_params.get("id"))
            serializer = MateriaSerializer(result, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Materia.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        """
        @queryparam: id
        """
        try:
            Materia.objects.filter(id=request.query_params.get("id")).delete()
            return Response(
                {"sms": "Periodo eliminado satisfactoriamente."},
                status=status.HTTP_200_OK,
            )
        except Materia.DoesNotExist:
            return Response(
                {"error": "No existe un periodo con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListMateria(ListAPIView):
    serializer_class = MateriaReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Materia.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Verifica si la queryset está vacía (caso específico según tus necesidades)
        if not self.request.user.is_authenticated:
            return Response(
                {"mensaje": "No tienes permiso para acceder a estos datos"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PeriodoLectivoAPI(generics.GenericAPIView):
    serializer_class = PeriodoLectivoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = PeriodoLectivoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            curso = PeriodoLectivo.objects.get(id=id)
            serializer = PeriodoLectivoSerializer(curso, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PeriodoLectivo.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="GET")
    def get(self, request, *args, **kwargs):
        """
        @queryparam: id
        """
        try:
            result = PeriodoLectivo.objects.get(id=request.query_params.get("id"))
            serializer = PeriodoLectivoSerializer(result, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PeriodoLectivo.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        """
        @queryparam: id
        """
        try:
            PeriodoLectivo.objects.filter(id=request.query_params.get("id")).delete()
            return Response(
                {"sms": "Periodo eliminado satisfactoriamente."},
                status=status.HTTP_200_OK,
            )
        except Curso.DoesNotExist:
            return Response(
                {"error": "No existe un periodo con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListAllPeriodo(ListAPIView):
    serializer_class = PeriodoLectivoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PeriodoLectivo.objects.all().order_by("periodo")


class LastPeriodo(ListAPIView):
    serializer_class = PeriodoLectivoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PeriodoLectivo.objects.last()


class MateriaCursoDocenteAPI(generics.GenericAPIView):
    serializer_class = MateriaCursoDocenteSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = MateriaCursoDocenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            curso = MateriaCursoDocente.objects.get(id=id)
            serializer = MateriaCursoDocenteSerializer(curso, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MateriaCursoDocente.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="GET")
    def get(self, request, *args, **kwargs):
        """
        @queryparam: id
        """
        try:
            result = MateriaCursoDocente.objects.get(id=request.query_params.get("id"))
            serializer = MateriaCursoDocenteSerializer(result, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MateriaCursoDocente.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        """
        @queryparam: id
        """
        try:
            result = MateriaCursoDocente.objects.filter(
                id=request.query_params.get("id")
            ).delete()
            return Response(
                {"sms": "Periodo eliminado satisfactoriamente."},
                status=status.HTTP_200_OK,
            )
        except MateriaCursoDocente.DoesNotExist:
            return Response(
                {"error": "No existe un periodo con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListMateriaCursoDocente(ListAPIView):
    serializer_class = MateriaCursoDocenteReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MateriaCursoDocente.objects.all().order_by("id")


class MateriaEstudianteAPI(generics.GenericAPIView):
    serializer_class = MateriaEstudianteSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = MateriaEstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            curso = MateriaCursoDocente.objects.get(id=id)
            serializer = MateriaEstudianteSerializer(curso, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MateriaEstudiante.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="GET")
    def get(self, request, *args, **kwargs):
        """
        @queryparam: id
        """
        try:
            result = MateriaEstudiante.objects.get(id=request.query_params.get("id"))
            serializer = MateriaEstudiante(result, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MateriaCursoDocente.DoesNotExist:
            return Response(
                {"error": "No existe un curso con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        """
        @queryparam: id
        """
        try:
            MateriaEstudiante.objects.filter(id=request.query_params.get("id")).delete()
            return Response(
                {"sms": "Periodo eliminado satisfactoriamente."},
                status=status.HTTP_200_OK,
            )
        except MateriaEstudiante.DoesNotExist:
            return Response(
                {"error": "No existe un periodo con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )
