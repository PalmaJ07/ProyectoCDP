from rest_framework import serializers
from .models import Doctor, Especialidad


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ["id", "descripcion"]


class DoctorSerializer(serializers.ModelSerializer):
    especialidades = EspecialidadSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", "nombre", "identificacion", "telefono", "estado", "precio", "especialidades"]
