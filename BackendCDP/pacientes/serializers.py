from rest_framework import serializers
from .models import Paciente, Historico

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            "id", "nombre", "sexo", "fecha_nacimiento", "identificacion",
            "edad", "telefono", "created_user", "update_user", "deleted_user"
        ]
        read_only_fields = ["created_user", "update_user", "deleted_user"]

# Serializer para Historico
class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = [
            "id",
            "paciente",     # se envía como id del paciente
            "fecha",
            "peso",
            "altura",
            "imc",
            "created_user",
            "update_user",
            "deleted_user"
        ]
        read_only_fields = ["created_user", "update_user", "deleted_user"]