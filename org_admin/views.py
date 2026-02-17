from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrgAdminCreatUserSerializer,AssineEmployToTeamleadSerializer,OrgAdminUserListSerializer
from rest_framework import status
from attendance.services import get_organisation
from account.models import User
from django.db.models import Q



class OrgAdminCreateUserAPIView(APIView):
    def post(self,request):
        if request.user.user_type !="ORG_ADMIN":
            return Response(
                {"error":"Permissin denied"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer=OrgAdminCreatUserSerializer(data=request.data,context={"request":request})
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User created succesfully"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, user_id=None):

        if request.user.user_type not in ["ORG_ADMIN","HR"]:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        org = get_organisation(request.user)

        # ---------- GET ONE USER ----------
        if user_id:
            try:
                user = User.objects.get(
                    Q(employee__organization=org) |
                    Q(hr__organization=org) |
                    Q(teamlead__organization=org) |
                    Q(accountent__organization=org) |
                    Q(organisation_admin__organization=org),
                    id=user_id
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found in this organisation"},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = OrgAdminUserListSerializer(
                user,
                context={"request": request}
            )
            return Response(serializer.data)

        # ---------- GET ALL USERS ----------
        users = User.objects.filter(
            Q(employee__organization=org) |
            Q(hr__organization=org) |
            Q(teamlead__organization=org) |
            Q(accountent__organization=org) |
            Q(organisation_admin__organization=org)
        ).distinct()

        serializer = OrgAdminUserListSerializer(
            users,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    
    def patch(self, request, user_id):
        if request.user.user_type != "ORG_ADMIN":
            return Response({"error": "Permission denied"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        # update user fields
        user.name = request.data.get("name", user.name)
        user.email = request.data.get("email", user.email)
        user.phone = request.data.get("phone", user.phone)
        user.individual_attendance_mode = request.data.get(
            "attendance_mode",
            user.individual_attendance_mode
        )
        user.save()

        # update profile
        profile = None
        if hasattr(user, "employee"):
            profile = user.employee
        elif hasattr(user, "hr"):
            profile = user.hr
        elif hasattr(user, "teamlead"):
            profile = user.teamlead
        elif hasattr(user, "accountent"):
            profile = user.accountent
        # elif hasattr(user, "organisation_admin"):
        #     profile = user.organisation_admin
        

        if profile:
            profile.department = request.data.get("department",
                                                  profile.department)
            profile.desigination = request.data.get("desigination",
                                                    profile.desigination)

            if request.FILES.get("photo"):
                profile.photo = request.FILES["photo"]

            if request.FILES.get("id_proof"):
                profile.id_proof = request.FILES["id_proof"]

            profile.save()

        return Response({"message": "User updated successfully"})
    
    def delete(self, request, user_id):
        if request.user.user_type != "ORG_ADMIN":
            return Response({"error": "Permission denied"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User deleted successfully"},
                        status=status.HTTP_200_OK)
        
        
class AssineEmployToTeamLeagAPIView(APIView):
    def post(self,request):
        if request.user.user_type not in ["ORG_ADMIN","HR"]:
            return Response(
                {"error":"Permissin denied"},
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer=AssineEmployToTeamleadSerializer(data=request.data,context={"request":request})
        
        if serializer.is_valid():
            employee=serializer.save()
            return Response({"message":"Employee assigned to Team Lead successfully","employ_id":employee.user.name,"team_lead":employee.team_lead.user.name},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)