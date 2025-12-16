from django.contrib import admin
from .models import Doctor, Especialidad


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion", "created_user", "update_user")
    search_fields = ("descripcion",)
    list_filter = ("created_user",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "nombre", 
        "identificacion", 
        "telefono", 
        "estado", 
        "precio", 
        "get_especialidades",  # 👈 método personalizado
        "created_user",
    )
    search_fields = ("nombre", "identificacion", "telefono")
    list_filter = ("estado", "especialidades")
    filter_horizontal = ("especialidades",)

    def get_especialidades(self, obj):
        return ", ".join([e.descripcion for e in obj.especialidades.all()])
    get_especialidades.short_description = "Especialidades"