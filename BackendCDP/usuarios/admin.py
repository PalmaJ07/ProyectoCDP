from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Usuario, TipoUsuario

# -------------------------------
# Formularios para Usuario
# -------------------------------

class UsuarioCreationForm(forms.ModelForm):
    """Formulario para crear un usuario en el admin"""
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ("usuario", "nombre", "identificacion", "tipo_usuario", "is_staff", "is_active")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hashea la contraseña
        if commit:
            user.save()
        return user


class UsuarioChangeForm(forms.ModelForm):
    """Formulario para cambiar un usuario existente en el admin"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Usuario
        fields = ("usuario", "nombre", "identificacion", "tipo_usuario", "password", "is_active", "is_staff", "is_superuser")


# -------------------------------
# Admin de TipoUsuario
# -------------------------------

@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("descripcion",)
    search_fields = ("descripcion",)


# -------------------------------
# Admin de Usuario
# -------------------------------

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario

    list_display = ("usuario", "nombre", "identificacion", "tipo_usuario", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "tipo_usuario")

    fieldsets = (
        (None, {"fields": ("usuario", "password")}),
        ("Información personal", {"fields": ("nombre", "identificacion", "tipo_usuario")}),
        ("Permisos", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Auditoría", {"fields": ("created_user", "update_user", "deleted_user")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("usuario", "nombre", "identificacion", "tipo_usuario", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("usuario", "nombre", "identificacion")
    ordering = ("usuario",)
