from django.contrib import admin
from .models import Arancel

@admin.register(Arancel)
class ArancelAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion", "precio", "tipo")
    search_fields = ("descripcion", "tipo")
    list_filter = ("tipo",)
    ordering = ("descripcion",)