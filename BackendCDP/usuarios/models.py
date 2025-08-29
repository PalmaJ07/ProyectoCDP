from django.db import models
from django.contrib.auth import get_user_model

# Usamos el modelo de usuario actual para los campos de auditoría
User = get_user_model()

class TipoUsuario(models.Model):
    descripcion = models.CharField(max_length=100)

    # Auditoría
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tipousuario_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tipousuario_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tipousuario_deleted')

    def __str__(self):
        return self.descripcion


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=128)
    
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, related_name='usuarios')

    # Auditoría
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='usuario_created')
    update_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='usuario_updated')
    deleted_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuario_deleted')

    def __str__(self):
        return self.nombre
