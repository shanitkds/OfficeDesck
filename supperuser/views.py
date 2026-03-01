from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import OrganisationSerializer
from organizations.models import Oganisation
from account.models import User
from org_admin.serializers import OrgAdminUserListSerializer
from django.shortcuts import get_object_or_404
from .servise import delete_organisation_with_all
from django.db.models import Q
from attendance.services import get_organisation


class OrganisationListAPIView(APIView):

    def get(self, request):

        if request.user.user_type not in  ["SUPER_ADMIN","ORG_ADMIN"]:
            return Response({"error": "Permission denied"}, status=403)

        org_id = request.query_params.get("org")

        if request.user.user_type =="SUPER_ADMIN":
            if org_id:
                try:
                    organisation = Oganisation.objects.get(id=org_id)
                    serializer = OrganisationSerializer(organisation)
                except Oganisation.DoesNotExist:
                    return Response({"error": "Organization not found"}, status=404)

            else:
                organisations = Oganisation.objects.all().order_by("-creates_at")
                serializer = OrganisationSerializer(organisations, many=True)
        elif request.user.user_type =="ORG_ADMIN":
            org=get_organisation(request.user)
            serializer = OrganisationSerializer(org)

        return Response(serializer.data)
    
    
    
class AdminUserListAPIView(APIView):

    def get(self, request):

        if request.user.user_type != "SUPER_ADMIN":
            return Response({"error": "Permission denied"}, status=403)

        org_id = request.query_params.get("org")

        if org_id:
            users = User.objects.filter(
                Q(employee__organization_id=org_id) |
                Q(hr__organization_id=org_id) |
                Q(teamlead__organization_id=org_id) |
                Q(accountent__organization_id=org_id) |
                Q(organisation_admin__organization_id=org_id)
            ).distinct()
        else:
            users = User.objects.all()

        serializer = OrgAdminUserListSerializer(users, many=True)
        return Response(serializer.data)
    
    

class OrganisationBlockAPIView(APIView):

    def post(self, request, org_id):

        if request.user.user_type != "SUPER_ADMIN":
            return Response({"error": "Permission denied"}, status=403)

        organisation = get_object_or_404(Oganisation, id=org_id)

        action = request.data.get("action")  
        if action == "block":
            organisation.is_active = False
            message = "Organization Blocked"

        elif action == "unblock":
            organisation.is_active = True
            message = "Organization Unblocked"

        else:
            return Response({"error": "Invalid action"}, status=400)

        organisation.save()

        return Response({"message": message})
    

class OrganisationDeleteAPIView(APIView):

    def delete(self, request, org_id):

        if request.user.user_type != "SUPER_ADMIN":
            return Response({"error": "Permission denied"}, status=403)

        org = get_object_or_404(Oganisation, id=org_id)

        delete_organisation_with_all(org)

        return Response({"message": "Organisation and all related data deleted"})