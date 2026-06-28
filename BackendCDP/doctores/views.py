from rest_framework import generics, permissions, filters
from django.db.models import Q
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# class DoctorListAPIView(generics.ListAPIView):
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = Doctor.objects.all().order_by("nombre")
#         search = self.request.query_params.get("search", None)
#         especialidad = self.request.query_params.get("especialidad", None)

#         if search:
#             queryset = queryset.filter(
#                 Q(nombre__icontains=search) |
#                 Q(identificacion__icontains=search) |
#                 Q(telefono__icontains=search)
#             )
#         if especialidad:
#             queryset = queryset.filter(especialidades__id=especialidad)

#         return queryset


class DoctorPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
    
class DoctorListAPIView(generics.ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DoctorPagination  # 👈 aquí

    def get_queryset(self):
        queryset = Doctor.objects.all().order_by("nombre")
        search = self.request.query_params.get("search", None)
        especialidad = self.request.query_params.get("especialidad", None)

        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(identificacion__icontains=search) |
                Q(telefono__icontains=search)
            )

        if especialidad:
            queryset = queryset.filter(especialidades__id=especialidad)

        return queryset
class DoctorNoPaginationAPIView(generics.ListAPIView):
    queryset = Doctor.objects.filter(deleted_user__isnull=True)
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Desactivar paginación
    pagination_class = None