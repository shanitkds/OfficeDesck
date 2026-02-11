from django.urls import path
from .views import TeamViewApi,TeamLeadReviewAPIView

urlpatterns = [
    path('view-membars/',TeamViewApi.as_view(),name="view-membars"),
    path('review/submit/',TeamLeadReviewAPIView.as_view(),name="review")
]