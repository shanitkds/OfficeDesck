from django.urls import path
from .views import SetFaceAPIView,MarkAttentanceAPIView,AttentanceRequestAPIView,AttendanceRequestActionAPIView,ManualAttendanceUpsertAPIView ,AttendanceViewAPI #,FaceVerfyAPIView,LiveLocationVerification


urlpatterns = [
    path('face-enroll/',SetFaceAPIView.as_view(),name="face-enroll"),
    path('mark-attentance/',MarkAttentanceAPIView.as_view(),name="mark-attentance"),
    path('attentance-request/',AttentanceRequestAPIView.as_view(),name="attentance-request"),
    path('attentance-requestaction/<int:re_id>/',AttendanceRequestActionAPIView.as_view(),name="attentance-request"),
    path('manual-attendance/',ManualAttendanceUpsertAPIView.as_view(),name='manual-attendance-upsert'),
    path('view/',AttendanceViewAPI.as_view(),name='manual-attendance-upsert')
    # path("face-verify/", FaceVerfyAPIView.as_view(), name="face-verify"),
    # path("verify-live-location/", LiveLocationVerification.as_view(), name="verify-live-location"),
]