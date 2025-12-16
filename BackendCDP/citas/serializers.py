from rest_framework import serializers
from .models import Cita


class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = [
            "id",
            "paciente",
            "paciente_nombre",
            "doctor_especialidad",
            "doctor_nombre",
            "arancel",
            "arancel_descripcion",
            "fecha_hora",
            "estado_pago",
            "estado",
            "created_user",
            "update_user",
            "deleted_user",
        ]
        read_only_fields = [
            "created_user",
            "update_user",
            "deleted_user",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["created_user"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["update_user"] = request.user
        return super().update(instance, validated_data)
