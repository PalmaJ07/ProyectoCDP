from django.urls import path
from .views import (
    ArancelListPaginatedAPIView,
    ArancelListNoPaginationAPIView,
    CrearFacturaAPIView,
    FacturaListAPIView
)

urlpatterns = [
    path("aranceles/", ArancelListPaginatedAPIView.as_view(), name="aranceles_paginados"),
    path("aranceles/all/", ArancelListNoPaginationAPIView.as_view(), name="aranceles_sin_paginacion"),
    path("facturas/crear/", CrearFacturaAPIView.as_view(), name="crear_factura"),
    path("facturas/", FacturaListAPIView.as_view(), name="listar_facturas"),
]