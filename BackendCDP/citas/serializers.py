from rest_framework import serializers
from .models import Cita, DetalleFactura, Arancel
from procedimientos.models import DetalleFactura


class CitaSerializer(serializers.ModelSerializer):

    factura = serializers.PrimaryKeyRelatedField(
        queryset=DetalleFactura.objects.all(),
        required=False,
        allow_null=True
    )

    arancel = serializers.PrimaryKeyRelatedField(
        queryset=Arancel.objects.all(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = Cita
        fields = [
            "id",
            "factura",
            "paciente",
            "paciente_nombre",
            "doctor_especialidad",
            "doctor_nombre",
            "arancel",
            "arancel_descripcion",
            "arancel_precio",
            "precio_final", 
            "debito_fijo",
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
        arancel = validated_data.get("arancel")


        if arancel:
            validated_data["arancel_precio"] = arancel.precio

        if request and request.user.is_authenticated:
            validated_data["created_user"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")

        #arancel = validated_data.get("arancel")    
        arancel = validated_data.get("arancel", instance.arancel.id)  # Mantener el arancel actual si no se proporciona uno nuevo
        detalle_actual = validated_data.get("factura",instance.factura)
        detalle_actual = detalle_actual.id if detalle_actual else None
        #detalle_actual = validated_data.get("factura")

        print("detalle_actual:", detalle_actual)
        print("arancel:", arancel)

    # buscar detalle factura
        detalle = DetalleFactura.objects.filter(
            factura=detalle_actual,
            id_arancel=arancel
        ).first()

        if detalle:
            validated_data["precio_final"] = detalle.arancel_precio

        if request and request.user.is_authenticated:
            validated_data["update_user"] = request.user

        return super().update(instance, validated_data)
