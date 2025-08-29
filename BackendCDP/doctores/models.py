from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Especialidad(models.Model):
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

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

    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_deleted')

    def __str__(self):
        return self.nombre

class DoctorEspecialidad(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='especialidades')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='doctores')
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctoresp_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctoresp_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctoresp_deleted')

    def __str__(self):
        return f'{self.doctor} - {self.especialidad}'

