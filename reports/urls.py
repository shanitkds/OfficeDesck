from django.urls import path
from .views import PerformanceListPDFAPIView,PaymentReportPDF,AttendanceReportPDF

urlpatterns=[
    path("performance/pdf/",PerformanceListPDFAPIView.as_view(),name="employeereport"),
    path("payment/pdf/",PaymentReportPDF.as_view()),
    path("attendance/pdf/", AttendanceReportPDF.as_view()),
]