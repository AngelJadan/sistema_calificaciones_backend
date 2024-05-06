from calificacion.models import MateriaEstudiante
from curso.serializer import MateriaEstudianteSerializer
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView


# Create your views here.
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
            curso = MateriaEstudianteSerializer.objects.get(id=id)
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


class ListEstudiantesCurso(ListAPIView):
    serializer_class = MateriaEstudianteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return MateriaEstudiante.objects.filter(
                materia_curso__curso=self.kwargs["curso"]
            ).order_by("id")
        else:
            return []
