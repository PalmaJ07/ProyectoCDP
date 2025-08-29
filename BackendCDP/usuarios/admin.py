from django.contrib import admin
from .models import Usuario, TipoUsuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'usuario', 'tipo_usuario', 'created_user', 'update_user', 'deleted_user']
    readonly_fields = ['created_user', 'update_user', 'deleted_user']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_user = request.user
        else:
            obj.update_user = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.deleted_user = request.user
        obj.save()
        super().delete_model(request, obj)

@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'created_user', 'update_user', 'deleted_user']
    readonly_fields = ['created_user', 'update_user', 'deleted_user']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_user = request.user
        else:
            obj.update_user = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.deleted_user = request.user
        obj.save()
        super().delete_model(request, obj)
