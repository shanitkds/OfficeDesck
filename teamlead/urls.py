from django.urls import path
from .views import TeamViewApi,TeamLeadReviewAPIView,UsersListAPIView

urlpatterns = [
    path('view-membars/',TeamViewApi.as_view(),name="view-membars"),
    path('review/submit/',TeamLeadReviewAPIView.as_view(),name="review"),
    path('userslist/',UsersListAPIView.as_view())
]