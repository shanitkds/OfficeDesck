from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import OrgAdminCreatUserSerializer,AssineEmployToTeamleadSerializer
from rest_framework import status


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
class AssineEmployToTeamLeagAPIView(APIView):
    def post(self,request):
        if request.user.user_type !="ORG_ADMIN":
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