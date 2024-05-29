from calificacion.models import (
    CabeceraTrimestre,
    Calificacion,
    MateriaEstudiante,
)
from persona.serializer import EstudianteSerializer
from rest_framework import serializers  # type: ignore


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


class CalificacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calificacion
        fields = "__all__"
        extra_kwargs = {"trimestre": {"required": False}}


class CabeceraTrimestreSerializer(serializers.ModelSerializer):
    calificacion_detalle = CalificacionSerializer(many=True, read_only=False)

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
            "calificacion_detalle",
        )

    def create(self, validated_data):
        calificacion_detalle = validated_data.pop("calificacion_detalle")
        new_trimestre = CabeceraTrimestre.objects.create(
            **validated_data,
        )

        for calificacion_detalle in calificacion_detalle:
            Calificacion.objects.create(**calificacion_detalle, trimestre=new_trimestre)
        return new_trimestre

    def update(self, CabeceraTrimestre, validated_data):

        calificacion_detalle = validated_data.get("calificacion_detalle")

        CabeceraTrimestre.numero_trimestre = validated_data.get("numero_trimestre")
        CabeceraTrimestre.materia_estudiante = validated_data.get("materia_estudiante")
        CabeceraTrimestre.aporte_cualitativo = validated_data.get("aporte_cualitativo")
        CabeceraTrimestre.proyecto_integrador = validated_data.get(
            "proyecto_integrador"
        )
        CabeceraTrimestre.cualitativo_proyecto_integrador = validated_data.get(
            "cualitativo_proyecto_integrador"
        )
        CabeceraTrimestre.usuario = validated_data.get("usuario")
        CabeceraTrimestre.save()

        Calificacion.objects.filter(trimestre=CabeceraTrimestre).delete()

        for calificacion in calificacion_detalle:
            Calificacion.objects.create(**calificacion, trimestre=CabeceraTrimestre)

        return CabeceraTrimestre


class CabeceraTrimestreReadSerializer(serializers.ModelSerializer):
    calificacion_detalle = CalificacionSerializer(many=True, read_only=False)

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
