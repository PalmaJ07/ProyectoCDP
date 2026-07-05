from urllib import request

from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Arancel, Factura, DetalleFactura
from .serializers import ArancelSerializer, DetalleFacturaSerializer, FacturaSerializer,FacturaDetalleCompletoSerializer

from rest_framework.generics import GenericAPIView, get_object_or_404
from .utils import filtrar_facturas_por_fecha

from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from xhtml2pdf import pisa
from .renderers import BinaryRenderer
from openpyxl import Workbook
from .renderers import BinaryRenderer
from django.utils.dateparse import parse_date
import openpyxl
from django.db.models import Sum

class FacturaBaseView(GenericAPIView):

    def get_filtered_queryset(self, request):
        queryset = Factura.objects.filter(deleted_user__isnull=True)
        queryset = filtrar_facturas_por_fecha(request, queryset)
        return queryset.order_by("-fecha")
    

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
        print(type(request.data))
        print(request.data)
        total = 0

        factura_serializer = FacturaSerializer(
            data={
                "id_paciente": data.get("id_paciente"),
                "fecha": data.get("fecha")
            },
            context={"request": request}
        )

        if not factura_serializer.is_valid():
            return Response(factura_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        factura = factura_serializer.save()

        detalles_data = data.get("detalles", [])
        detalles_creados = []

        for item in detalles_data:
            arancel = get_object_or_404(Arancel, id=item["id_arancel"])

            precio = item.get("precio", arancel.precio)
            total += precio

            detalle = DetalleFactura.objects.create(
                factura=factura,
                id_arancel=arancel,
                arancel_descripcion=arancel.descripcion,
                arancel_tipo=arancel.tipo,
                arancel_precio=precio,
                created_user=request.user
            )

            detalles_creados.append(DetalleFacturaSerializer(detalle).data)


        factura.total = total
        factura.save()



        return Response({
            "factura": FacturaSerializer(factura).data,
            "detalles": detalles_creados
        }, status=status.HTTP_201_CREATED)

# ---------------------------------------------
# API #4 — Listar facturas con su desglose
# ---------------------------------------------
# class FacturaListAPIView(FacturaBaseView, generics.ListAPIView):
#     serializer_class = FacturaDetalleCompletoSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return self.get_filtered_queryset(self.request)

class FacturaListAPIView(FacturaBaseView, generics.ListAPIView):
    serializer_class = FacturaDetalleCompletoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.get_filtered_queryset(self.request)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # 🔥 SUMA TOTAL DE TODAS LAS FACTURAS (sin paginación)
        total_general = queryset.aggregate(total=Sum('total'))['total'] or 0

        # 🔹 Aplicar paginación normalmente
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)

            # 🔥 Agregar el total general a la respuesta
            response.data['total_general'] = total_general
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "results": serializer.data,
            "total_general": total_general
        })

class FacturaPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Factura.objects.filter(deleted_user__isnull=True)

        fecha = request.query_params.get("fecha")
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")

        if fecha:
            queryset = queryset.filter(fecha=parse_date(fecha))

        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(
                fecha__range=[
                    parse_date(fecha_inicio),
                    parse_date(fecha_fin)
                ]
            )

        template = get_template("reportes/facturas_pdf.html")
        html = template.render({"facturas": queryset})

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="facturas.pdf"'

        pisa.CreatePDF(html, dest=response)
        return response
    
class FacturaExcelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Factura.objects.filter(deleted_user__isnull=True)

        fecha = request.query_params.get("fecha")
        fecha_inicio = request.query_params.get("fecha_inicio")
        fecha_fin = request.query_params.get("fecha_fin")

        if fecha:
            queryset = queryset.filter(fecha=parse_date(fecha))

        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(
                fecha__range=[
                    parse_date(fecha_inicio),
                    parse_date(fecha_fin)
                ]
            )

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Facturas"

        ws.append([
            "Factura ID",
            "Fecha",
            "Total",
            "Arancel",
            "Tipo",
            "Precio"
        ])

        for factura in queryset:
            for d in factura.detalles.all():
                ws.append([
                    factura.id,
                    factura.fecha,
                    factura.total,
                    d.arancel_descripcion,
                    d.arancel_tipo,
                    d.arancel_precio
                ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="facturas.xlsx"'

        wb.save(response)
        return response