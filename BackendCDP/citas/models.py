from django.db import models
from django.conf import settings
from pacientes.models import Paciente
from doctores.models import Doctor
from procedimientos.models import Arancel, DetalleFactura


class Cita(models.Model):
    factura = models.ForeignKey(
        DetalleFactura,
        on_delete=models.SET_NULL,  # o CASCADE según tu lógica
        null=True,
        blank=True,
        related_name="citas"
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="citas"
    )
    paciente_nombre = models.CharField(max_length=100)

    doctor_especialidad = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="citas"
    )
    doctor_nombre = models.CharField(max_length=50)

    arancel = models.ForeignKey(
        Arancel,
        on_delete=models.SET_NULL,
        null=True,
        related_name="citas"
    )
    arancel_descripcion = models.CharField(max_length=255)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    arancel_precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    debito_fijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=250.00)
    fecha_hora = models.DateTimeField()

    estado_pago = models.BooleanField(default=False)
    estado = models.CharField(max_length=50)

    # Auditoría
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cita_created'
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='cita_updated'
    )
    deleted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cita_deleted'
    )

    def __str__(self):
        return f"Cita #{self.id} - {self.paciente_nombre}"
