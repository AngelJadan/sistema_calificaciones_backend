from calificacion.models import MateriaEstudiante
from rest_framework import serializers


class MateriaEstudianteSerializer(serializers.ModelSerializer):
    class Meta:

        model = MateriaEstudiante
        fields = "__all__"

    def update(self, MateriaEstudiante, validated_data):
        return super().update(MateriaEstudiante, validated_data)
