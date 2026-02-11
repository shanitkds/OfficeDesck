from django.urls import path
from .views import GenaratePerformenceAPIView,ViewPerformenceAPIView


urlpatterns=[
    path('emplyee-performance/',GenaratePerformenceAPIView.as_view(),name="performance"),
    path('performance-reports/',ViewPerformenceAPIView.as_view(),name="performance-reports")
]




# GET /api/performance/performance-reports/?month=February&year=2026