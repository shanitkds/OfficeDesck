from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrganisationRegistrationSerialiser,SetLocationSerializer
from rest_framework.permissions import AllowAny


class OrganisationRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self,request):
        seralizer=OrganisationRegistrationSerialiser(data=request.data)
        
        if seralizer.is_valid():
            seralizer.save()
            return Response(
                {"message": "Organization and Admin created successfully"},
                status=status.HTTP_201_CREATED
            )
            
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SetofficeLocationAPIView(APIView):
    def patch(self,request):
        if request.user.user_type !='ORG_ADMIN':
            return Response({"error":"you have no access to use this"},status=status.HTTP_403_FORBIDDEN)
        org=request.user.organisation_admin.organization
        
        serializer=SetLocationSerializer(org,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data":serializer.data,"message": "Office location updated successfully"},status=status.HTTP_200_OK)
        return Response({"not valid"},status=status.HTTP_400_BAD_REQUEST)
        
        