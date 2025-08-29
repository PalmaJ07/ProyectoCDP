from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    sexo = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    identificacion = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()
    telefono = models.CharField(max_length=20)

    # Auditoría
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='paciente_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='paciente_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='paciente_deleted')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
