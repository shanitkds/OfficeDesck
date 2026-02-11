from django.contrib import admin
from django.urls import path
from .views import FileUploadAPIView,FileViewAPIView,ExportFileAPIView,ShareFileViewAPIView,ShareFileDownloadAPIView

urlpatterns = [
    path('upload/',FileUploadAPIView.as_view(),name='upload'),
    path('<int:fl_id>/view/',FileViewAPIView.as_view(),name='view'),
    path('<int:fl_id>/export/',ExportFileAPIView.as_view(),name='export'), #download and share
    path('<int:share_id>/share-view/',ShareFileViewAPIView.as_view(),name='share-view'), 
    path('<int:share_id>/share-download/',ShareFileViewAPIView.as_view(),name='share-download'), 
]