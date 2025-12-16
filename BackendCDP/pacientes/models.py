from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
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

class Historico(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='historicos')
    fecha = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)   # kg
    altura = models.DecimalField(max_digits=5, decimal_places=2) # cm
    imc = models.DecimalField(max_digits=5, decimal_places=2)    # índice de masa corporal

    # Auditoría (opcional, igual que en Paciente)
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='historico_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='historico_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='historico_deleted')

    def __str__(self):
        return f"Histórico de {self.paciente.nombre} - {self.fecha}"