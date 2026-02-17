from django.urls import path
from .views import PerformanceListPDFAPIView

urlpatterns=[
    path("performance/pdf/",PerformanceListPDFAPIView.as_view(),name="employeereport")
]