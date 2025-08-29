from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'sexo', 'identificacion', 'edad', 'telefono')
    search_fields = ('nombre', 'apellido', 'identificacion')
    list_filter = ('sexo',)

