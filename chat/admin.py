from django.contrib import admin
from .models import ChatRoom,ChatGroup,ChatGroupMember,Message,GroupMessage

# Register your models here.
admin.site.register(ChatRoom)
admin.site.register(ChatGroup)
admin.site.register(ChatGroupMember)
admin.site.register(Message)
admin.site.register(GroupMessage)
