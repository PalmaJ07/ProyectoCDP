from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UsuarioManager(BaseUserManager):
    def create_user(self, usuario, contrasena=None, **extra_fields):
        if not usuario:
            raise ValueError("El campo usuario es obligatorio")
        user = self.model(usuario=usuario, **extra_fields)
        user.set_password(contrasena)  # Hashea la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, usuario, contrasena=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(usuario, contrasena, **extra_fields)


class TipoUsuario(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50)
    usuario = models.CharField(max_length=50, unique=True)

    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, related_name="usuarios", null=True, blank=True)

    # Campos obligatorios para Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Auditoría
    created_user = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="usuario_created"
    )
    update_user = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="usuario_updated"
    )
    deleted_user = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="usuario_deleted"
    )

    objects = UsuarioManager()

    USERNAME_FIELD = "usuario"
    REQUIRED_FIELDS = ["nombre", "identificacion"]

    def __str__(self):
        return self.nombre
