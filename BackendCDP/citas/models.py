from django.db import models
from django.contrib.auth import get_user_model
from pacientes.models import Paciente
from doctores.models import Especialidad, Doctor  # según tus apps actuales

User = get_user_model()

class TipoEstadoProceso(models.Model):
    descripcion = models.CharField(max_length=100)

    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tipoestado_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tipoestado_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tipoestado_deleted')

    def __str__(self):
        return self.descripcion


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='citas')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateTimeField()
    estado_pago = models.BooleanField(default=False)
    estado_proceso = models.ForeignKey(TipoEstadoProceso, on_delete=models.CASCADE, related_name='citas')

    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cita_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cita_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cita_deleted')

    def __str__(self):
        return f"Cita de {self.paciente} con {self.doctor} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
