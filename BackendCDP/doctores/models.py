from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Especialidad(models.Model):
    descripcion = models.CharField(max_length=100)

    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='especialidad_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='especialidad_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='especialidad_deleted')

    def __str__(self):
        return self.descripcion


class Doctor(models.Model):
    nombre = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # 👈 Precio único del doctor
    especialidades = models.ManyToManyField("Especialidad", related_name="doctores")  # 👈 Relación directa

    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_deleted')

    def __str__(self):
        return self.nombre
