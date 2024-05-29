from calificacion.models import (
    CabeceraTrimestre,
    Calificacion,
    MateriaEstudiante,
)
from calificacion.serializer import (
    CabeceraTrimestreReadSerializer,
    CabeceraTrimestreSerializer,
    MateriaEstudianteAllSerializer,
    MateriaEstudianteSerializer,
)
from curso.models import MateriaCursoDocente
from curso.serializer import (
    MateriaEstudianteReadSerializer,
)
from rest_framework import status, generics  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.generics import ListAPIView  # type: ignore
from rest_framework.decorators import api_view  # type: ignore


# Create your views here.
class MateriaEstudianteAPI(generics.GenericAPIView):
    serializer_class = MateriaEstudianteSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = MateriaEstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            curso = MateriaEstudiante.objects.get(id=id)
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
        except MateriaEstudiante.DoesNotExist:
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


class TrimestreEstudianteAPI(generics.GenericAPIView):
    serializer_class = CabeceraTrimestreSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = CabeceraTrimestreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            curso = CabeceraTrimestre.objects.get(id=id)
            serializer = CabeceraTrimestreSerializer(curso, data=request.data)
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


class ListEstudiantesMateria(ListAPIView):
    serializer_class = MateriaEstudianteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MateriaEstudiante.objects.filter(
                materia_curso__materia=self.kwargs["materia"]
            ).order_by("id")
        else:
            return []


class ListEstudiantesCurso(ListAPIView):
    serializer_class = MateriaEstudianteReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MateriaEstudiante.objects.filter(
                materia_curso__curso=self.kwargs["curso"]
            ).order_by("id")
        else:
            return []


class ListPeriodoCurso(ListAPIView):
    serializer_class = MateriaEstudianteReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MateriaEstudiante.objects.filter(
            materia_curso__periodo_lectivo=self.kwargs["periodo"]
        ).order_by("id")


class ListMateriaEstudiantes(ListAPIView):
    serializer_class = MateriaEstudianteSerializer

    def get_queryset(self):
        return MateriaEstudiante.objects.filter(
            materia_curso=self.kwargs["curso_materia"]
        )


@api_view(["get"])
def list_estudiantes_calificaciones(request, curso_materia):
    cabecera_trimestre = CabeceraTrimestre.objects.get(
        materia_estudiante__id=curso_materia
    )
    detalle_trimestre = Calificacion.objects.filter(
        cabecera_trimestre=cabecera_trimestre
    )


class CabeceraTrimestreAPI(generics.GenericAPIView):
    serializer_class = CabeceraTrimestreSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request):
        serializer = CabeceraTrimestreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, method="PUT")
    def put(self, request):
        id = request.data.get("id")
        try:
            trimestre = CabeceraTrimestre.objects.get(id=id)
            serializer = CabeceraTrimestreSerializer(trimestre, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CabeceraTrimestre.DoesNotExist:
            return Response(
                {"error": "No existe un trimestre con este id."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="GET")
    def get(self, request, *args, **kwargs):
        """
        @queryparam: id
        """
        try:
            result = CabeceraTrimestre.objects.get(id=request.query_params.get("id"))
            serializer = CabeceraTrimestre(result, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CabeceraTrimestre.DoesNotExist:
            return Response(
                {"error": "No existe un trimestre con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, method="DELETE")
    def delete(self, request):
        """
        @queryparam: id
        """
        try:
            CabeceraTrimestre.objects.filter(id=request.query_params.get("id")).delete()
            return Response(
                {"sms": "Periodo eliminado satisfactoriamente."},
                status=status.HTTP_200_OK,
            )
        except MateriaEstudiante.DoesNotExist:
            return Response(
                {"error": "No existe un periodo con este id"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListEstudianteCabeceraTrimestre(ListAPIView):
    serializer_classes = CabeceraTrimestreReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CabeceraTrimestre.objects.filter(
            materia_estudiante__estudiante=self.kwargs["estudante"]
        ).order_by("id")


@api_view(["GET"])
def api_view(request, curso_materia):
    try:
        materia_in_curso = MateriaEstudiante.objects.filter(materia_curso=curso_materia)
        serializers = MateriaEstudianteAllSerializer(materia_in_curso, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    except MateriaCursoDocente.DoesNotExist:
        return Response(
            {"error": "No existe un curso con este id"},
            status=status.HTTP_400_BAD_REQUEST,
        )
