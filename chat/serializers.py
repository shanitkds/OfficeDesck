from rest_framework import serializers
from .models import Message,ChatRoom,GroupMessage,ChatGroup
from secure_files.servise import get_user_image

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.name", read_only=True)
    sender = serializers.IntegerField(source="sender.id", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "sender_name", "text", "is_read", "created_at"]
        

class ChatRoomListSerializer(serializers.ModelSerializer):
    chat_with = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()   # ⭐ NEW

    class Meta:
        model = ChatRoom
        fields = ["id", "chat_with", "created_at", "unread_count"]

    def get_chat_with(self, obj):
        request = self.context.get("request")
        user = request.user

        other = obj.user2 if obj.user1 == user else obj.user1

        return {
            "id": other.id,
            "name": other.name,
            "user_type": other.user_type,
            "image": get_user_image(other, request)
        }

    def get_unread_count(self, obj):
        request = self.context.get("request")
        user = request.user

        return obj.messages.filter(
            is_read=False
        ).exclude(sender=user).count()
    
class GroupMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(
        source="sender.name",
        read_only=True
    )
    class Meta:
        model = GroupMessage
        fields = ["id", "sender_name", "text", "created_at"]
        
class ChatGroupListSrializer(serializers.ModelSerializer):
    class Meta:
        model=ChatGroup
        fields=["id","name","created_at"]