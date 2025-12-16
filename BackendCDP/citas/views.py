from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date
from datetime import datetime, time
from django.utils.timezone import make_aware, get_current_timezone
from .models import Cita
from .serializers import CitaSerializer

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

class CitaListAPIView(generics.ListAPIView):
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]

    # 🔍 Buscar SOLO por paciente
    search_fields = [
        "paciente_nombre",
    ]

    # 🎯 Filtros exactos
    filterset_fields = [
        "doctor_especialidad",
        "estado",
        "estado_pago",
    ]

    def get_queryset(self):
        queryset = Cita.objects.filter(deleted_user__isnull=True)

        fecha = self.request.query_params.get("fecha")
        fecha_inicio = self.request.query_params.get("fecha_inicio")
        fecha_fin = self.request.query_params.get("fecha_fin")

        tz = get_current_timezone()

        # 📅 RANGO DE FECHAS (PRIORIDAD)
        if fecha_inicio and fecha_fin:
            inicio = make_aware(
                datetime.combine(
                    datetime.strptime(fecha_inicio, "%Y-%m-%d").date(),
                    time.min
                ),
                tz
            )
            fin = make_aware(
                datetime.combine(
                    datetime.strptime(fecha_fin, "%Y-%m-%d").date(),
                    time.max
                ),
                tz
            )

            queryset = queryset.filter(
                fecha_hora__gte=inicio,
                fecha_hora__lte=fin
            )

        # 📅 UNA SOLA FECHA
        elif fecha:
            inicio = make_aware(
                datetime.combine(
                    datetime.strptime(fecha, "%Y-%m-%d").date(),
                    time.min
                ),
                tz
            )
            fin = make_aware(
                datetime.combine(
                    datetime.strptime(fecha, "%Y-%m-%d").date(),
                    time.max
                ),
                tz
            )

            queryset = queryset.filter(
                fecha_hora__gte=inicio,
                fecha_hora__lte=fin
            )

        return queryset.order_by("-fecha_hora")