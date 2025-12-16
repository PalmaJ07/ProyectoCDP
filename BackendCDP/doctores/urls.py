from django.urls import path
from .views import DoctorListAPIView,DoctorNoPaginationAPIView

urlpatterns = [
    path("index/", DoctorListAPIView.as_view(), name="doctor-list"),
    path("index2/", DoctorNoPaginationAPIView.as_view(), name="doctor-list-np"),
    
]