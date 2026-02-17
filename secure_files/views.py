from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SecureFile,FileShare
from attendance.services import get_organisation
from .permissions.file_permissions import can_view_file,can_downlaod_file,can_share_file,file_delete_permition
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from account.models import User
from django.db.models import Q
from .permissions.encryption import genarate_file_KEY,encrpt_file,decript_file,encrypt_key,decript_key

from django.core.files.base import ContentFile
from django.http import HttpResponse

from .serializers import SecureFileSerializer,ShareHistorySerializer,SharedWithMeSerializer
from .servise import get_user_image




class FileUploadAPIView(APIView):
    def post(self,request):
        user=request.user
        upladed_file=request.FILES.get('file')
        if not upladed_file or not user:
            return Response("uploaded file and user requerd",status=status.HTTP_400_BAD_REQUEST)
        
        file_bite=upladed_file.read()
        file_key=genarate_file_KEY()
        encrypted_bytes=encrpt_file(file_bite,file_key)
        encrypt_file_key=encrypt_key(file_key)
        
        encrypted_content=ContentFile(encrypted_bytes)
        encrypted_content.name=upladed_file.name
        
        secure_file=SecureFile.objects.create(
            original_name=upladed_file.name,
            file_type=upladed_file.name.split(".")[-1],
            mime_type=upladed_file.content_type,
            encrypted_file=encrypted_content,
            encrypted_file_key=encrypt_file_key,
            owner=user,
            owner_role=user.user_type,
            team_lead=getattr(getattr(user,'employee',None),'team_lead',None),
            organization=get_organisation(user),
            allow_view=True,
            allow_download=True,
            allow_share=True
            
        )
        
        
        
        return Response({"message": "File uploaded successfully","file_id": secure_file.id,"file_name": secure_file.original_name,},
                        status=status.HTTP_201_CREATED,
                        )
        
class FileViewAPIView(APIView):
    def get(self,request,fl_id):
        user=request.user
        try:
            file=SecureFile.objects.get(id=fl_id)
        except SecureFile.DoesNotExist:
            return Response("File not exixt",status=status.HTTP_404_NOT_FOUND)
        
        if not can_view_file(user,file):
            return Response("You have no pemission",status=status.HTTP_403_FORBIDDEN)
        
        file_key=decript_key(file.encrypted_file_key)
        encrypt_bytes=file.encrypted_file.read()
        decript_bytes=decript_file(encrypt_bytes,file_key)
        
        response = HttpResponse(
            decript_bytes,
            content_type=file.mime_type
        )
        response["Content-Disposition"] = (
            f'inline; filename="{file.original_name}"'
        )
        
        
        return response
        
class ExportFileAPIView(APIView):
    def get(self,request,fl_id):  #downlod
        user=request.user
        try:
            file=SecureFile.objects.get(id=fl_id)
        except SecureFile.DoesNotExist:
            return Response("File not exixt",status=status.HTTP_404_NOT_FOUND)
        if not can_downlaod_file(user,file):
            return Response("You have no pemission",status=status.HTTP_403_FORBIDDEN)
        
        file_key=decript_key(file.encrypted_file_key)
        encrypt_bytes=file.encrypted_file.read()
        decript_bytes=decript_file(encrypt_bytes,file_key)
        
        response = HttpResponse(
            decript_bytes,
            content_type=file.mime_type
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{file.original_name}"'
        )
        
        
        return response


    def post(self,request,fl_id): #Share
        user=request.user
        
        try:
            file=SecureFile.objects.get(id=fl_id)
        except SecureFile.DoesNotExist:
            return Response("File not exixt",status=status.HTTP_404_NOT_FOUND)
        
        if not can_share_file(user,file):
            return Response("You have no pemission",status=status.HTTP_403_FORBIDDEN)
        
        
        shared_with_id=request.data.get('shared_with')
        message=request.data.get('message',"")
        can_view=request.data.get('can_view',True)
        can_download =request.data.get('can_download',False)
        
        if not shared_with_id:
            return Response(
                {"error": "shared_with is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        shared_with=get_object_or_404(User,id=shared_with_id)
        sh_or=get_organisation(shared_with)
        
        if sh_or !=file.organization:
            return Response(
                {"error": "Cannot share file outside organisation"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if FileShare.objects.filter(
            file=file,
            shared_with=shared_with
        ).exists():
            return Response(
                {"error": "File already shared with this user"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        FileShare.objects.create(
            file=file,
            shared_with=shared_with,
            message=message,
            can_view=bool(can_view),
            can_download=bool(can_download),
            shared_by=user
        )
        
        return Response({'File shared successfully'},status=status.HTTP_201_CREATED)
    
    
class ShareFileViewAPIView(APIView):
    def get(self,request,share_id):
        user=request.user
        
        file_share=FileShare.objects.get(
            Q(id=share_id),
            Q(shared_with=user)|Q(shared_by=user),
            can_view=True
            )
        
        if not file_share:
            return Response({"This file not in this"},status=status.HTTP_404_NOT_FOUND)
        
        file=file_share.file
        
        
        if not can_view_file(user,file):
            return Response(
                {"error": "You do not have permission to view this file"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        file_key=decript_key(file.encrypted_file_key)
        encrypt_byte=file.encrypted_file.read()
        decrypt_bytes=decript_file(encrypt_byte,file_key)
        
        response = HttpResponse(
            decrypt_bytes,
            content_type=file.mime_type
        )
        response["Content-Disposition"] = (
            f'inline; filename="{file.original_name}"'
        )
        
        return response
    
class ShareFileDownloadAPIView(APIView):
    def get(self,request,share_id):
        user=request.user
        
        file_share=FileShare.objects.get(
            Q(id=share_id),
            Q(shared_with=user)|Q(shared_by=user),
            can_view=True
            )
        
        if not file_share:
            return Response({"This file not in this"},status=status.HTTP_404_NOT_FOUND)
        
        file=file_share.file
        
        if not can_downlaod_file(user,file):
            return Response(
                {"error": "You do not have permission to download this file"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        file_key=decript_key(file.encrypted_file_key)
        encrypt_byte=file.encrypted_file.read()
        decrypt_bytes=decript_file(encrypt_byte,file_key)
            
        response = HttpResponse(
            decrypt_bytes,
            content_type=file.mime_type
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{file.original_name}"'
        )
        
        return response
    
    
class AddSharedFileToSecureFilesAPIView(APIView):
    def post(self,request,file_id):
        user=request.user
        file_share=get_object_or_404(
            FileShare,
            Q(id=file_id),
            Q(shared_with=user) | Q(shared_by=user),
            can_view=True,
            can_download=True
            )
        
        file=file_share.file
        
        if SecureFile.objects.filter(
            owner=user,
            encrypted_file=file.encrypted_file
        ).exists():
            return Response({"error": "File already added to your files"},status=status.HTTP_400_BAD_REQUEST)
        
        
        new_file=SecureFile.objects.create(
            original_name=file.original_name,
            file_type=file.file_type,
            mime_type=file.mime_type,
            encrypted_file=file.encrypted_file,
            owner=user,
            owner_role=user.user_type,
            team_lead=getattr(getattr(user,'employee',None),'team_lead',None),
            organization=file.organization,
            allow_view=True,
            allow_download=True,
            allow_share=True
        )
        
        return Response({"message": "File added to your files successfully","file_id": new_file.id},status=status.HTTP_201_CREATED)
    
    def delete(self,request, file_id):  #File delete section
        user = request.user
        file_obj=get_object_or_404(SecureFile,id=file_id)
        if not file_delete_permition(user,file_obj):
            return Response(
                {"error": "You do not have permission to delete this file"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        file_obj.delete()
        return Response(
            {"message": "File deleted successfully"},
            status=status.HTTP_200_OK
        )
        


class MyFilesAPIView(APIView):

    def get(self, request):
        user = request.user
        org = get_organisation(user)

        filter_type = request.GET.get("type", "all")
       
        if user.user_type == "ORG_ADMIN":

            if filter_type == "my":
                files = SecureFile.objects.filter(owner=user)

            else:  
                files = SecureFile.objects.filter(organization=org)

       
        elif user.user_type == "TEAM_LEAD":

            teamlead_obj = getattr(user, "teamlead", None)

            team_files = SecureFile.objects.filter(team_lead=teamlead_obj)
            own_files = SecureFile.objects.filter(owner=user)

            if filter_type == "my":
                files = own_files
            else:
                files = (team_files | own_files).distinct()

       
        else:
            files = SecureFile.objects.filter(owner=user)

        serializer = SecureFileSerializer(
            files,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    
class SharedFilesAPIView(APIView):

    def get(self, request):
        user = request.user

        shared_with_me = FileShare.objects.filter(
            shared_with=user
        ).select_related(
            "file",
            "file__owner",
            "shared_by"
        )

        serializer = SharedWithMeSerializer(
            shared_with_me,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    
    
class ShareHistoryAPIView(APIView):

    def get(self, request):
        user = request.user

        if user.user_type != "ORG_ADMIN":
            return Response(
                {"error": "Permission denied"},
                status=403
            )

        org = get_organisation(user)

        history = FileShare.objects.filter(
            file__organization=org
        ).select_related("file", "shared_with", "shared_by")

        serializer = ShareHistorySerializer(history, many=True)
        return Response(serializer.data)



class ShareAllowedUsersAPIView(APIView):

    def get(self, request, file_id):
        current_user = request.user
        org = get_organisation(current_user)

       
        if current_user.user_type == "EMPLOYEE":
            return Response([])

        if current_user.user_type in ["ORG_ADMIN", "HR", "ACCOUNTANT"]:
            users = User.objects.filter(
                Q(employee__organization=org) |
                Q(hr__organization=org) |
                Q(teamlead__organization=org) |
                Q(accountent__organization=org) |
                Q(organisation_admin__organization=org)   # ✅ FIXED TYPO
            ).distinct()

        elif current_user.user_type == "TEAM_LEAD":
            users = User.objects.filter(
                employee__team_lead=current_user.teamlead
            )

        else:
            users = User.objects.none()

        data = []

        for u in users:
            if u == current_user:
                continue

            image_url = get_user_image(u, request)

            data.append({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "user_type": u.user_type,
                "image": image_url,
            })

        return Response(data)