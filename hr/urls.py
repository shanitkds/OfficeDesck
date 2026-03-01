from django.urls import path
from .views import EmployeeRequestManageAPIView

urlpatterns = [
    path("user-creation-request/",EmployeeRequestManageAPIView.as_view()),
    path("user-creation-request/<int:id>/",EmployeeRequestManageAPIView.as_view()),
]