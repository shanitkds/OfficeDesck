from django.urls import path
from .views import *

urlpatterns = [
    path('login/',LoginAPIView.as_view(),name="login"),
    path('oradmin_dash/',OrAdminDashboardAPIView.as_view(),name="login"),
    path('teamlead/',TeamLeadAPIView.as_view()),
    path('employee/',EmployeeAPIView.as_view()),
    path('hr/',HrAPIView.as_view()),
    path('accountent/',AccountentAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),
    path("forgot-password/", ForgotPasswordAPI.as_view()),
    path("reset-password/<uid>/<token>/", ResetPasswordAPI.as_view()),
]