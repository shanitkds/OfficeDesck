from django.urls import path
from .views import SentPrivetMessageApi,GetPrivetAPIView,ChatRoomListAPIView,GroupManageAPIView,AddGruopMemberAPIView,RemoveGroupAPIView,RemovememberAPIView,GroupeMessageSentAPIView,GroupeMessageGetAPIView,ChatGroupListAPIView
urlpatterns = [
    path('send/',SentPrivetMessageApi.as_view(),name="send"),
    path('messages/<int:room_id>/',GetPrivetAPIView.as_view(),name="pr-messages"),
    path('rooms/',ChatRoomListAPIView.as_view(),name="rooms"),
    path('group/create/',GroupManageAPIView.as_view(),name="rooms"),
    path('group/add/',AddGruopMemberAPIView.as_view(),name="add-mamber"),
    path('group/remove/<int:group_id>/<int:user_id>/',RemovememberAPIView.as_view(),name="add-mamber"),
    path('group/delete/<int:group_id>/',RemoveGroupAPIView.as_view(),name="gr-delete"),
    path('group/sent/',GroupeMessageSentAPIView.as_view(),name="gr-sent"),
    path('group/messages/<int:gr_id>/',GroupeMessageGetAPIView.as_view(),name="gr-messages"),
    path('group/list/',ChatGroupListAPIView.as_view(),name="gr-list"),
]