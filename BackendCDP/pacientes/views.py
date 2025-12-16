from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Paciente, Historico
from .serializers import PacienteSerializer,HistoricoSerializer

# Paginador personalizado
class PacientePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 50


# Crear Paciente (POST)
class PacienteCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PacienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_user=request.user, update_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Listar Pacientes con paginación y búsqueda (GET)
class PacienteListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        search = request.query_params.get("search", "")
        pacientes = Paciente.objects.filter(
            Q(nombre__icontains=search),
            deleted_user__isnull=True   # 👈 solo activos
        ).order_by("id")

        paginator = PacientePagination()
        result_page = paginator.paginate_queryset(pacientes, request)
        serializer = PacienteSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# Actualizar Paciente (PUT)
class PacienteUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            paciente = Paciente.objects.get(pk=pk)
        except Paciente.DoesNotExist:
            return Response({"error": "Paciente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PacienteSerializer(paciente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(update_user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Eliminar Paciente (DELETE lógico)
class PacienteDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            paciente = Paciente.objects.get(pk=pk, deleted_user__isnull=True)
        except Paciente.DoesNotExist:
            return Response({"error": "Paciente no encontrado o ya eliminado"}, status=status.HTTP_404_NOT_FOUND)

        paciente.deleted_user = request.user
        paciente.save()
        return Response({"message": "Paciente marcado como eliminado"}, status=status.HTTP_200_OK)

class HistoricoListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, paciente_id):
        try:
            paciente = Paciente.objects.get(pk=paciente_id, deleted_user__isnull=True)
        except Paciente.DoesNotExist:
            return Response({"error": "Paciente no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        historicos = Historico.objects.filter(
            paciente=paciente,
            deleted_user__isnull=True
        ).order_by('-fecha')  # del más reciente al más antiguo

        serializer = HistoricoSerializer(historicos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Crear un nuevo registro Historico (POST)
class HistoricoCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = HistoricoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_user=request.user, update_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)