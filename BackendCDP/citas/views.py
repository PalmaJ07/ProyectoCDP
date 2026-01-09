from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date
from datetime import datetime, time
from django.utils.timezone import make_aware, get_current_timezone

from citas.renderers import BinaryRenderer
from .models import Cita
from .serializers import CitaSerializer

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook
from rest_framework.generics import GenericAPIView

class CitaBaseFilterView(GenericAPIView):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]

    search_fields = ["paciente_nombre"]

    filterset_fields = [
        "doctor_especialidad",
        "estado",
        "estado_pago",
    ]

    def get_filtered_queryset(self, request):
        queryset = Cita.objects.filter(deleted_user__isnull=True)
        queryset = filtrar_citas(request, queryset)

        for backend in self.filter_backends:
            queryset = backend().filter_queryset(
                request, queryset, self
            )

        return queryset.order_by("-fecha_hora")

class CitaCreateAPIView(generics.CreateAPIView):
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]

class CitaUpdateAPIView(generics.UpdateAPIView):
    queryset = Cita.objects.filter(deleted_user__isnull=True)
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]

class CitaDeleteAPIView(generics.DestroyAPIView):
    queryset = Cita.objects.filter(deleted_user__isnull=True)
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cita = self.get_object()
        cita.deleted_user = request.user
        cita.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CitaListAPIView(CitaBaseFilterView, generics.ListAPIView):
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.get_filtered_queryset(self.request)
    
class CitaPDFAPIView(CitaBaseFilterView, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = self.get_filtered_queryset(request)

        template = get_template("reportes/citas_pdf.html")
        html = template.render({"citas": queryset})

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="citas.pdf"'

        pisa.CreatePDF(html, dest=response)
        return response

class CitaExcelAPIView(CitaBaseFilterView, APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [BinaryRenderer]  # ✅ CLAVE

    def get(self, request):
        queryset = self.get_filtered_queryset(request)

        wb = Workbook()
        ws = wb.active
        ws.title = "Citas"

        ws.append([
            "Paciente",
            "Doctor",
            "Especialidad",
            "Fecha",
            "Estado",
            "Estado Pago"
        ])

        for c in queryset:
            ws.append([
                c.paciente_nombre,
                c.doctor_nombre,
                c.arancel_descripcion,
                c.fecha_hora.strftime("%d/%m/%Y %H:%M"),
                c.estado,
                c.estado_pago
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="citas.xlsx"'

        wb.save(response)
        return response
    
def filtrar_citas(request, queryset):
    fecha = request.query_params.get("fecha")
    fecha_inicio = request.query_params.get("fecha_inicio")
    fecha_fin = request.query_params.get("fecha_fin")

    tz = get_current_timezone()

    if fecha_inicio and fecha_fin:
        inicio = make_aware(
            datetime.combine(
                datetime.strptime(fecha_inicio, "%Y-%m-%d").date(),
                time.min
            ), tz
        )
        fin = make_aware(
            datetime.combine(
                datetime.strptime(fecha_fin, "%Y-%m-%d").date(),
                time.max
            ), tz
        )
        queryset = queryset.filter(fecha_hora__gte=inicio, fecha_hora__lte=fin)

    elif fecha:
        inicio = make_aware(
            datetime.combine(
                datetime.strptime(fecha, "%Y-%m-%d").date(),
                time.min
            ), tz
        )
        fin = make_aware(
            datetime.combine(
                datetime.strptime(fecha, "%Y-%m-%d").date(),
                time.max
            ), tz
        )
        queryset = queryset.filter(fecha_hora__gte=inicio, fecha_hora__lte=fin)

    return queryset