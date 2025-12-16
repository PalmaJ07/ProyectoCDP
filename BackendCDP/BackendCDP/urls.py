from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.urls')),
    path('api/doctores/', include('doctores.urls')),
    path("api/pacientes/", include("pacientes.urls")),
    path("api/procedimientos/", include("procedimientos.urls")),
    path("api/citas/", include("citas.urls")),
]

