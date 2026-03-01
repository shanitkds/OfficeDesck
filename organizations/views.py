from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SetLocationSerializer,OrganizationRequestSerializer
from rest_framework.permissions import AllowAny
from django.db import transaction
from .models import OrganizationRequest,Oganisation
from .service import create_org_and_admin_from_request
from .util.registeremail import send_org_request_status_mail


# class OrganisationRegistrationAPIView(APIView):
#     permission_classes = [AllowAny]
#     authentication_classes = []
    
#     def post(self,request):
#         seralizer=OrganisationRegistrationSerialiser(data=request.data)
        
#         if seralizer.is_valid():
#             seralizer.save()
#             return Response(
#                 {"message": "Organization and Admin created successfully"},
#                 status=status.HTTP_201_CREATED
#             )
            
#         return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
        
class CreateOrganizationRequest(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data.copy()
        data["requested_by"] = request.user.id

        serializer = OrganizationRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Organization request submitted"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateOrganizationRequestStatus(APIView):

    def post(self, request, pk):
        if request.user.user_type != "SUPER_ADMIN":
            return Response({"error": "Permission denied"}, status=403)

        try:
            org_req = OrganizationRequest.objects.get(id=pk)
        except OrganizationRequest.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        new_status = request.data.get("status")

        if new_status not in ["APPROVED", "REJECTED"]:
            return Response({"error": "Invalid status"}, status=400)

        if org_req.status == "APPROVED":
            return Response({"error": "Already approved"}, status=400)

        if Oganisation.objects.filter(email=org_req.org_email).exists():
            return Response({"error": "Organization already exists"}, status=400)

        with transaction.atomic():

            org_req.status = new_status
            org_req.approved_by = request.user

            if new_status == "REJECTED":
                org_req.rejection_reason = request.data.get("reason", "")
                org_req.save()
                send_org_request_status_mail(org_req)
                return Response({"message": "Request Rejected"})

            organisation = create_org_and_admin_from_request(org_req)

            org_req.save()
            send_org_request_status_mail(org_req)

        return Response({"message": "Approved & Organization Created"})
    

class OrganizationRequestList(APIView):

    def get(self, request):
        user=request.user
        if user.user_type != "SUPER_ADMIN":
            return Response({"error": "Permission denied"}, status=403)
        data = OrganizationRequest.objects.filter(status="PENDING").order_by("-created_at")
        serializer = OrganizationRequestSerializer(data, many=True)
        return Response(serializer.data)