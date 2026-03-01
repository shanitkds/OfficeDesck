from django.urls import path
from .views import *

urlpatterns=[
    path("organisationslist/", OrganisationListAPIView.as_view()),
    path("userslist/", AdminUserListAPIView.as_view()),
    path("organisation/<int:org_id>/block/", OrganisationBlockAPIView.as_view()),
    path("organisation/<int:org_id>/delete/", OrganisationDeleteAPIView.as_view()),
]