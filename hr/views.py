from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from .models import EmployeeRequest
from .serializers import EmployeeRequestSerializer,EmployeeRequestSerializerView
from account.models import User
from employee.models import Employee
from teamlead.models import TeamLead
from accountant.models import Accountent
from hr.models import HR
from attendance.services import get_organisation
import uuid
from org_admin.serializers import copy_file



class EmployeeRequestManageAPIView(APIView):

    def post(self, request):
        user = request.user
        if user.user_type != "HR":
            return Response(
                {"error": "Not allowed"},
                status=403
            )

        serializer = EmployeeRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(requested_by=request.user)
            return Response(
                {"message": "Request sent to Admin"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=400)
    
    def get(self, request):

        user = request.user

        if user.user_type == "ORG_ADMIN":
            data = EmployeeRequest.objects.filter(
                status="PENDING"
            ).order_by("-created_at")

        elif user.user_type == "HR":
            data = EmployeeRequest.objects.filter(
                requested_by=user
            ).order_by("-created_at")

        else:
            return Response(
                {"error": "Not allowed"},
                status=403
            )

        serializer = EmployeeRequestSerializerView(data, many=True)
        return Response(serializer.data)
    


    def patch(self, request, id):

        # ✅ Only Org Admin allowed
        if request.user.user_type != "ORG_ADMIN":
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        req = get_object_or_404(EmployeeRequest, id=id)

        new_status = request.data.get("status")

        if new_status not in ["APPROVED", "REJECTED"]:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Update status first
        req.status = new_status
        req.save()

        if new_status != "APPROVED":
            return Response({"message": "Request Rejected"})

        # ===============================
        # ORGANISATION
        # ===============================
        org = request.user.organisation_admin.organization

        # ===============================
        # COPY FILES (SAFE)
        # ===============================
        photo_file = copy_file(req.photo)
        id_file = copy_file(req.id_proof)

        # ===============================
        # CREATE USER
        # ===============================
        if req.action == "CREATE":

            employee_id = f"{req.user_type[:2]}-{uuid.uuid4().hex[:6]}"

            user = User.objects.create_user(
                name=req.name,
                email=req.email,
                password=req.password,
                employee_id=employee_id,
                user_type=req.user_type,
                phone=req.phone,
                individual_attendance_mode=req.attendance_mode
            )

        # ===============================
        # UPDATE USER
        # ===============================
        elif req.action == "UPDATE":

            if not req.employee_id:
                return Response(
                    {"error": "employee_id required for update"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.filter(employee_id=req.employee_id).first()

            if not user:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            user.name = req.name
            user.email = req.email
            user.phone = req.phone
            user.user_type = req.user_type
            user.individual_attendance_mode = req.attendance_mode

            user.save()

        else:
            return Response({"error": "Invalid action"}, status=400)

        # ===============================
        # UPDATE PROFILE TABLE
        # ===============================
        defaults = {
            "organization": org
        }

        if photo_file:
            defaults["photo"] = photo_file

        if id_file:
            defaults["id_proof"] = id_file

        if req.department:
            defaults["department"] = req.department

        if req.designation:
            defaults["desigination"] = req.designation


        if req.user_type == "EMPLOYEE":
            Employee.objects.update_or_create(user=user, defaults=defaults)

        elif req.user_type == "TEAM_LEAD":
            TeamLead.objects.update_or_create(user=user, defaults=defaults)

        elif req.user_type == "HR":
            HR.objects.update_or_create(user=user, defaults=defaults)

        elif req.user_type == "ACCOUNTANT":
            Accountent.objects.update_or_create(user=user, defaults=defaults)

        return Response({
            "message": f"Request {new_status} completed successfully"
        })
