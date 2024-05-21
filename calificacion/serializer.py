from calificacion.models import (
    CabeceraActividad,
    CabeceraTrimestre,
    DetalleActividad,
    DetalleTrimestre,
    MateriaEstudiante,
)
from persona.serializer import EstudianteSerializer
from rest_framework import serializers


class MateriaEstudianteSerializer(serializers.ModelSerializer):
    class Meta:

        model = MateriaEstudiante
        fields = "__all__"

    def update(self, MateriaEstudiante, validated_data):
        return super().update(MateriaEstudiante, validated_data)


class MateriaEstudianteReadSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer(many=False, read_only=False)

    class Meta:
        model = MateriaEstudiante
        fields = "__all__"
        depth = 1


class DetalleActividadSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetalleActividad
        fields = "__all__"


class CabeceraActividadSerializer(serializers.ModelSerializer):
    detalle_actividad = DetalleActividadSerializer(many=True, read_only=False)

    class Meta:
        model = CabeceraActividad
        fields = "__all__"


class DetalleTrimesterSerializer(serializers.ModelSerializer):
    cabecera_actividad = CabeceraActividadSerializer(many=True, read_only=False)

    class Meta:
        model = DetalleTrimestre
        fields = "__all__"


class CabeceraTrimestreSerializer(serializers.ModelSerializer):
    cabecera_trimestre = DetalleTrimesterSerializer(many=False, read_only=False)

    class Meta:
        model = CabeceraTrimestre
        fields = (
            "id",
            "numero_trimestre",
            "materia_estudiante",
            "aporte_cualitativo",
            "proyecto_integrador",
            "cualitativo_proyecto_integrador",
            "usuario",
            "cabecera_trimestre",
        )

    def create(self, validated_data):
        cabecera_trimestre = validated_data.pop("cabecera_trimestre")

        for detalle in cabecera_trimestre.pop("detalle_trimestre"):
            pass


class CabeceraTrimestreReadSerializer(serializers.ModelSerializer):
    detalle_trimestre = DetalleTrimesterSerializer(many=True, read_only=False)

    class Meta:
        model = CabeceraTrimestre
        fields = "__all__"


class MateriaEstudianteAllSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSerializer(many=False, read_only=False)
    estudiante_trimestre = CabeceraTrimestreReadSerializer(many=True, read_only=False)

    class Meta:
        model = MateriaEstudiante
        fields = "__all__"
        depth = 1
