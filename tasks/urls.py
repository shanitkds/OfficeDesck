from django.urls import path
from .views import GetPostTaskManageAPIView,TaskGetApiView,TaskSubmitView,ApproverDeletView

urlpatterns = [
    path('task_manage/',GetPostTaskManageAPIView.as_view(),name="task_manage"),
    path('uniq_task_manage/<int:id>',TaskGetApiView.as_view(),name="uniq_task_manage"),
    path('task_submit/<int:id>',TaskSubmitView.as_view(),name="task_submit"),
    path('task_approve/<int:id>',ApproverDeletView.as_view(),name="task_approve"),
]