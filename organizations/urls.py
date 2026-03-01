from django.urls import path
from .views import *

urlpatterns = [
    path('set-location/',SetofficeLocationAPIView.as_view(),name="set-location"),
    path("org-request/create/", CreateOrganizationRequest.as_view()),
    path("org-request/list/", OrganizationRequestList.as_view()),
    path("org-request/status/<int:pk>/", UpdateOrganizationRequestStatus.as_view()),
]