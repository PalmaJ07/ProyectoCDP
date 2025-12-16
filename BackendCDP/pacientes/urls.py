from django.urls import path
from .views import (
    PacienteCreateAPIView, PacienteListAPIView,
    PacienteUpdateAPIView, PacienteDeleteAPIView,
    HistoricoListAPIView,HistoricoCreateAPIView
)

urlpatterns = [
    path("create/", PacienteCreateAPIView.as_view(), name="paciente-create"),
    path("index/", PacienteListAPIView.as_view(), name="paciente-list"),
    path("update/<int:pk>/", PacienteUpdateAPIView.as_view(), name="paciente-update"),
    path("delete/<int:pk>/", PacienteDeleteAPIView.as_view(), name="paciente-delete"),
    path('historicos/<int:paciente_id>/', HistoricoListAPIView.as_view(), name='historico-list'),  # GET historicos de un paciente
    path('historicos/create/', HistoricoCreateAPIView.as_view(), name='historico-create'), 
]
