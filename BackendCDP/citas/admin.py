from django.contrib import admin
from .models import TipoEstadoProceso, Cita

@admin.register(TipoEstadoProceso)
class TipoEstadoProcesoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ('descripcion',)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'especialidad', 'doctor', 'fecha', 'estado_pago', 'estado_proceso')
    list_filter = ('estado_pago', 'estado_proceso', 'fecha')
    search_fields = ('paciente__nombre', 'paciente__apellido', 'doctor__nombre')
