from django.contrib import admin
from .models import Doctor, Especialidad, DoctorEspecialidad

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'identificacion', 'telefono', 'estado', 'created_user', 'update_user', 'deleted_user']
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


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'precio', 'created_user', 'update_user', 'deleted_user']
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


@admin.register(DoctorEspecialidad)
class DoctorEspecialidadAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'especialidad', 'precio', 'created_user', 'update_user', 'deleted_user']
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
