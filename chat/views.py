from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from account.models import User
from .permissions import same_organisation,can_private_chat,can_create_group,can_add_employee_to_group
from .models import ChatRoom,Message,ChatGroup,ChatGroupMember,GroupMessage
from attendance.services import get_organisation
from .serializers import MessageSerializer,ChatRoomListSerializer,GroupMessageSerializer,ChatGroupListSrializer
from django.db.models import Q



class SentPrivetMessageApi(APIView):
    def post(self,request):
        sender=request.user
        receiver_id=request.data.get("receiver_id")
        text=request.data.get("text")
        
        if not receiver_id or not text:
            return Response({"detail": "receiver_id and text required"}, status=status.HTTP_400_BAD_REQUEST)
        
        receiver=get_object_or_404(User,id=receiver_id)
        
        if not same_organisation(sender,receiver):
            return Response({"detail": "Different organization"},status=status.HTTP_403_FORBIDDEN)
        
        if not can_private_chat(sender,receiver):
            return Response({"detail": "Chat not allowed"},status=status.HTTP_403_FORBIDDEN)
        
        org=get_organisation(sender)
        room,_=ChatRoom.objects.get_or_create(
            organization=org,
            user1=min(sender,receiver,key=lambda x:x.id),
            user2=max(sender,receiver,key=lambda x:x.id)
        )
        
        Message.objects.create(
            room=room,
            sender=sender,
            text=text
        )
        
        return Response({"detail": "Message sent", "room_id": room.id})
    
class GetPrivetAPIView(APIView):
    def get(self,request,room_id):
        user=request.user
        
        room=get_object_or_404(ChatRoom,id=room_id)
        
        if user not in [room.user1,room.user2]:
            return Response({"detail": "Access denied"},status=status.HTTP_403_FORBIDDEN)
        
        message=room.messages.order_by("created_at")
        Message.objects.filter(
            room_id=room_id,
            is_read=False
        ).exclude(sender=user).update(is_read=True)

            
        data=MessageSerializer(message,many=True).data
        return Response(data)
        
class ChatRoomListAPIView(APIView):
    def get(self,request):
        user=request.user
        org=get_organisation(user)
        
        room=ChatRoom.objects.filter(
            Q(user1=user)|Q(user2=user),
            organization=org
        ).order_by("-created_at")
        
        print(room)
        serializer=ChatRoomListSerializer(room,many=True,context={"request": request})
        return Response(serializer.data)


# groop chact section

class GroupManageAPIView(APIView):
    def post(self,request):
        user=request.user
        if not can_create_group(user):
            return Response({"detail": "Only Team Lead can create group"},status=status.HTTP_403_FORBIDDEN)
        
        group_name=request.data.get("name")
        if not group_name:
            return Response({"detail": "Group name is required"},status=status.HTTP_400_BAD_REQUEST)
        
        org=get_organisation(user)
        group=ChatGroup.objects.create(
            name=group_name,
            created_by=user,
            organization=org
        )
        
        ChatGroupMember.objects.create(
            group=group,
            user=user
            
        )
        
        org_admins = User.objects.filter(
            user_type="ORG_ADMIN",
            organisation_admin__organization=org
        )
        
        for admin in org_admins:
            ChatGroupMember.objects.create(
                group=group,
                user=admin
            )
        
        return Response({
            "detail": "Group created successfully",
            "group_id": group.id,
        })
        
        
        
class AddGruopMemberAPIView(APIView):  #Add a member in to group
    def post(self, request):
        user=request.user
        group_id = request.data.get("group_id")
        user_ids = request.data.get("user_ids", [])
        
        if not group_id or not user_ids:
            return Response(
                {"detail": "group_id and user_ids list required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        group = ChatGroup.objects.filter(id=group_id).first()
        if not group:
            return Response({"detail": "Group not found"}, status=404)
        
        if group.created_by!=user:
            return Response(
                {"detail": "Only group creator can add members"},
                status=403
            )
        
        added = []
        skipped = []
        
        for id in user_ids:
            employee=User.objects.filter(id=id).first()
            if not employee:
                skipped.append(id)
                continue
            
            if get_organisation(employee) != get_organisation(user):
                skipped.append(id)
                continue
            
            
            if not can_add_employee_to_group(user, employee):
                skipped.append(id)
                continue
            
            if ChatGroupMember.objects.filter(group=group, user=employee).exists():
                skipped.append(id)
                continue
            
            ChatGroupMember.objects.create(
                group=group,
                user=employee
            )
            
            added.append(id)
            
        return Response({
            "detail": "Bulk add completed",
            "added_users": added,
            "skipped_users": skipped
        })
        
        
class RemovememberAPIView(APIView):

    def delete(self, request, group_id, user_id):
        print("hello")
        user = request.user

        group = ChatGroup.objects.filter(id=group_id).first()
        if not group:
            return Response(
                {"detail": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if get_organisation(user) != group.organization:
            return Response(
                {"detail": "Different organization"},
                status=status.HTTP_403_FORBIDDEN
            )

        is_creator = group.created_by == user
        is_org_admin = user.user_type == "ORG_ADMIN"

        if not (is_creator or is_org_admin):
            return Response(
                {"detail": "You do not have permission to remove members"},
                status=status.HTTP_403_FORBIDDEN
            )

        member = ChatGroupMember.objects.filter(
            group=group,
            user_id=user_id
        ).first()

        if not member:
            return Response(
                {"detail": "User not in group"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if member.user.user_type == "ORG_ADMIN":
            return Response(
                {"detail": "You can't remove org admin"},
                status=status.HTTP_403_FORBIDDEN
            )

        member.delete()

        return Response(
            {"detail": "Member removed successfully"},
            status=status.HTTP_200_OK
        )
    

class RemoveGroupAPIView(APIView):
    def delete(self, request, group_id):  #this for delete group
        user = request.user
        group = ChatGroup.objects.filter(id=group_id).first()
        
        if not group:
            return Response(
                {"detail": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if get_organisation(user) != group.organization:
            return Response(
                {"detail": "Different organization"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        is_creator = group.created_by == user
        is_org_admin = user.user_type == "ORG_ADMIN"
        
        if not (is_creator or is_org_admin):
            return Response(
                {"detail": "You do not have permission to delete this group"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        group.delete()
        
        return Response({
            "detail": "Group deleted successfully"
        })
        
class GroupeMessageSentAPIView(APIView):
    def post(self, request):
        user=request.user
        group_id = request.data.get("group_id")
        text = request.data.get("text")
        
        if not group_id or not text:
            return Response(
                {"detail": "group_id and text required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        group=get_object_or_404(ChatGroup,id=group_id)
        if not group:
            return Response(
                {"detail": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if get_organisation(user) !=group.organization:
            return Response(
                {"detail": "Different organization"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        is_member = ChatGroupMember.objects.filter(
            group=group,
            user=user
        ).exists()

        if not is_member:
            return Response(
                {"detail": "You are not a member of this group"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        message=GroupMessage.objects.create(
            group=group,
            sender=user,
            text=text
        )
        
        return Response({
            "detail": "Message sent",
            "message_id": message.id,
            "message":text
        })
        
    def get(self, request):
        user=request.user
        org=get_organisation(user)
        
        group=ChatGroup.objects.filter(
            organization=org,
            chatgroupmember__user=user
        )
      
class GroupeMessageGetAPIView(APIView):
    def get(self, request,gr_id):
        user=request.user
        
        group=get_object_or_404(ChatGroup,id=gr_id)
        if not group:
            return Response(
                {"detail": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )
            
        if get_organisation(user)!=group.organization:
            return Response(
                {"detail": "Different organization"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        if not get_object_or_404(ChatGroupMember,group=group,user=user):
            return Response(
                {"detail": "You are not a member of this group"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        messages = group.messages.order_by("created_at")
        serializer = GroupMessageSerializer(messages, many=True)
        return Response(serializer.data)

class ChatGroupListAPIView(APIView):
    def get(self,request):
        user=request.user
        org=get_organisation(user)

        
        groups=ChatGroup.objects.filter(
            organization=org,
            chatgroupmember__user=user
        ).order_by("-created_at")
        
        serializer=ChatGroupListSrializer(groups,many=True)
        return Response(serializer.data)