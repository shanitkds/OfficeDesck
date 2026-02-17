from django.urls import path
from .views import LoginAPIView,OrAdminDashboardAPIView

urlpatterns = [
    path('login/',LoginAPIView.as_view(),name="login"),
    path('oradmin_dash/',OrAdminDashboardAPIView.as_view(),name="login")
]