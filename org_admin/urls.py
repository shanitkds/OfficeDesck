from django.urls import path
from .views import OrgAdminCreateUserAPIView,AssineEmployToTeamLeagAPIView

urlpatterns = [
    path('oruser_creation/',OrgAdminCreateUserAPIView.as_view(),name="oruser_creation"),
    path('team_lead_assine/',AssineEmployToTeamLeagAPIView.as_view(),name="team_lead_assine")
]