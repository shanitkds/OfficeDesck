from django.db import models
from account.models import User
from organizations.models import Oganisation


class ChatRoom(models.Model):
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE,related_name="chat_rooms")
    user1=models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_user1")
    user2=models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_user2")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("organization", "user1", "user2")
    
    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}---{self.id}"
    
    
class Message(models.Model):
    room=models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name='messages')
    sender =models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} : {self.text[:20]}"
    
class ChatGroup(models.Model):
    organization=models.ForeignKey(Oganisation,on_delete=models.CASCADE,related_name="chat_groups")
    name=models.CharField(max_length=100)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id}-{self.name}"
    
class ChatGroupMember(models.Model):
    group=models.ForeignKey(ChatGroup,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("group", "user")
    
class GroupMessage(models.Model):
    group=models.ForeignKey(ChatGroup,on_delete=models.CASCADE,related_name="messages")
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
