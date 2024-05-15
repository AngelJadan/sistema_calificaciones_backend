from calificacion.models import MateriaEstudiante
from calificacion.serializer import MateriaEstudianteReadSerializer
from curso.models import (
    Area,
    Curso,
    Materia,
    MateriaCursoDocente,
    Paralelo,
    PeriodoLectivo,
)
from persona.serializer import EstudianteSerializer
from rest_framework import serializers


class ParaleloReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paralelo
        fields = "__all__"
        depth = 1


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"

    def update(self, Curso, validated_data):
        return super().update(Curso, validated_data)


class CursoSerializerRead(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = "__all__"
        depth = 1


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"

    def update(self, Area, validated_data):
        return super().update(Area, validated_data)


class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = "__all__"


class MateriaReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = "__all__"
        depth = 1


class PeriodoLectivoSerializer(serializers.ModelSerializer):
    class Meta:
        def validate_periodo(self):
            if self["periodo"] < 1:
                raise serializers.ValidationError(
                    {"periodo": "El periodo no puede ser menor a cero"}
                )

        def validate_inicio_fin_periodo(self):
            if self["periodo_abierto"] == self["cierre_periodo"]:
                raise serializers.ValidationError(
                    {"periodo_abierto": "La fecha de periodo no pueden ser igual"}
                )

        model = PeriodoLectivo
        fields = "__all__"
        validators = [validate_periodo, validate_inicio_fin_periodo]

    def update(self, CursoDocente, validated_data):
        return super().update(CursoDocente, validated_data)


class MateriaCursoDocenteReadSerializer(serializers.ModelSerializer):
    materia_curso = MateriaEstudianteReadSerializer(many=True, read_only=False)

    class Meta:
        model = MateriaCursoDocente
        fields = (
            "id",
            "curso",
            "periodo_lectivo",
            "materia",
            "docente",
            "materia_curso",
        )
        depth = 2


class MateriaCursoDocenteSerializer(serializers.ModelSerializer):
    class Meta:

        model = MateriaCursoDocente
        fields = "__all__"

    def update(self, MateriaCursoDocente, validated_data):
        return super().update(MateriaCursoDocente, validated_data)
