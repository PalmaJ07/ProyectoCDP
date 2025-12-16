from rest_framework import serializers
from .models import Arancel, Factura, DetalleFactura


# ---------------------------------------------
# Arancel
# ---------------------------------------------
class ArancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arancel
        fields = [
            "id",
            "descripcion",
            "precio",
            "tipo",
            "created_user",
            "update_user",
            "deleted_user",
        ]
        read_only_fields = ["created_user", "update_user", "deleted_user"]

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


# ---------------------------------------------
# Factura
# ---------------------------------------------
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = [
            "id",
            "id_paciente",
            "fecha",
            "total",
            "created_user",
            "update_user",
            "deleted_user",
        ]
        read_only_fields = ["created_user", "update_user", "deleted_user"]

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


# ---------------------------------------------
# Detalle Factura
# ---------------------------------------------
class DetalleFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleFactura
        fields = [
            "id",
            "factura",
            "id_arancel",
            "arancel_descripcion",
            "arancel_tipo",
            "arancel_precio",
            "created_user",
            "update_user",
            "deleted_user",
        ]
        read_only_fields = ["created_user", "update_user", "deleted_user"]

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
    
class FacturaDetalleCompletoSerializer(serializers.ModelSerializer):
    detalles = DetalleFacturaSerializer(many=True, read_only=True)

    class Meta:
        model = Factura
        fields = [
            "id",
            "id_paciente",
            "fecha",
            "total",
            "detalles"
        ]
