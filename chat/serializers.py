from rest_framework import serializers
from .models import Message,ChatRoom,GroupMessage,ChatGroup

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)
    
    class Meta:
        model=Message
        fields=["id","sender_name","text","is_read","created_at"]
        

class ChatRoomListSerializer(serializers.ModelSerializer):
    chat_with=serializers.SerializerMethodField()
    
    class Meta:
        model=ChatRoom
        fields=["id","chat_with","created_at"]
    
    def get_chat_with(self, obj):
        request = self.context.get("request")
        user = request.user
        
        if obj.user1 == user:
            return obj.user2.name
        return obj.user1.name
    
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