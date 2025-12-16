from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Arancel, Factura, DetalleFactura
from .serializers import ArancelSerializer, DetalleFacturaSerializer, FacturaSerializer,FacturaDetalleCompletoSerializer
from django.utils.dateparse import parse_date

# ---------------------------------------------
# API #1 — Aranceles con paginación, search, filtro por tipo
# ---------------------------------------------
class ArancelListPaginatedAPIView(generics.ListAPIView):
    queryset = Arancel.objects.filter(deleted_user__isnull=True)
    serializer_class = ArancelSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]

    # Filtro por tipo
    filterset_fields = ["tipo"]

    # Search en descripcion y tipo
    search_fields = ["descripcion", "tipo"]

# ---------------------------------------------
# API #2 — Aranceles sin paginación + search
# ---------------------------------------------
class ArancelListNoPaginationAPIView(generics.ListAPIView):
    queryset = Arancel.objects.filter(deleted_user__isnull=True)
    serializer_class = ArancelSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

        # Filtro por tipo
    filterset_fields = ["tipo"]

    search_fields = ["descripcion", "tipo"]

    # Desactivar paginación
    pagination_class = None

from rest_framework.response import Response
from rest_framework import status, views


# ---------------------------------------------
# API #3 — Crear factura estilo carrito
# ---------------------------------------------
class CrearFacturaAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data

        # 1. Validar datos de factura
        factura_serializer = FacturaSerializer(
            data={
                "id_paciente": data.get("id_paciente"),
                "fecha": data.get("fecha"),
                "total": data.get("total")
            },
            context={"request": request}
        )

        if not factura_serializer.is_valid():
            return Response(factura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        factura = factura_serializer.save()

        # 2. Crear los detalles
        detalles_data = data.get("detalles", [])
        detalles_creados = []

        for item in detalles_data:
            arancel = Arancel.objects.get(id=item["id_arancel"])

            detalle = DetalleFactura.objects.create(
                factura=factura,
                id_arancel=arancel,
                arancel_descripcion=arancel.descripcion,
                arancel_tipo=arancel.tipo,
                arancel_precio=arancel.precio,
                created_user=request.user
            )

            detalles_creados.append(DetalleFacturaSerializer(detalle).data)

        return Response({
            "factura": FacturaSerializer(factura).data,
            "detalles": detalles_creados
        }, status=status.HTTP_201_CREATED)

# ---------------------------------------------
# API #4 — Listar facturas con su desglose
# ---------------------------------------------
class FacturaListAPIView(generics.ListAPIView):
    queryset = Factura.objects.filter(deleted_user__isnull=True)
    serializer_class = FacturaDetalleCompletoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Factura.objects.filter(deleted_user__isnull=True)

        fecha = self.request.query_params.get("fecha")
        fecha_inicio = self.request.query_params.get("fecha_inicio")
        fecha_fin = self.request.query_params.get("fecha_fin")

        # 📅 Una sola fecha
        if fecha:
            queryset = queryset.filter(fecha=parse_date(fecha))

        # 📅 Rango de fechas
        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(
                fecha__range=[
                    parse_date(fecha_inicio),
                    parse_date(fecha_fin)
                ]
            )

        return queryset.order_by("-fecha")
