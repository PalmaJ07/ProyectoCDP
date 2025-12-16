from django.urls import path
from .views import (
    CitaCreateAPIView,
    CitaUpdateAPIView,
    CitaDeleteAPIView,
    CitaListAPIView
)

urlpatterns = [
    path("crear/", CitaCreateAPIView.as_view(), name="cita_crear"),
    path("editar/<int:pk>/", CitaUpdateAPIView.as_view(), name="cita_editar"),
    path("eliminar/<int:pk>/", CitaDeleteAPIView.as_view(), name="cita_eliminar"),
    path("", CitaListAPIView.as_view(), name="cita_listar"),
]
