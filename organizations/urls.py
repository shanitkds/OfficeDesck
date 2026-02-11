from django.urls import path
from .views import OrganisationRegistrationAPIView,SetofficeLocationAPIView

urlpatterns = [
    path('register/',OrganisationRegistrationAPIView.as_view(),name="org-register"),
    path('set-location/',SetofficeLocationAPIView.as_view(),name="set-location")
]