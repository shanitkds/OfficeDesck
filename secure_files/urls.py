from django.contrib import admin
from django.urls import path
from .views import FileUploadAPIView,FileViewAPIView,ExportFileAPIView,ShareFileViewAPIView,ShareFileDownloadAPIView,MyFilesAPIView,SharedFilesAPIView,ShareHistoryAPIView,ShareAllowedUsersAPIView,AddSharedFileToSecureFilesAPIView

urlpatterns = [
    path('upload/',FileUploadAPIView.as_view(),name='upload'),
    path('<int:fl_id>/view/',FileViewAPIView.as_view(),name='view'),
    path('<int:fl_id>/export/',ExportFileAPIView.as_view(),name='export'), #download and share
    path('<int:share_id>/share-view/',ShareFileViewAPIView.as_view(),name='share-view'), 
    path('<int:share_id>/share-download/',ShareFileDownloadAPIView.as_view(),name='share-download'), 
    path('file-list-view/',MyFilesAPIView.as_view(),name='share-download'), 
    path('sharefileView/',SharedFilesAPIView.as_view(),name='share-download'), 
    path('share-history/',ShareHistoryAPIView.as_view(),name='share-download'), 
    path("share-users/<int:file_id>/", ShareAllowedUsersAPIView.as_view()),
    path("add-sharefile/<int:file_id>/",AddSharedFileToSecureFilesAPIView.as_view())
]