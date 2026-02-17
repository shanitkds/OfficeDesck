from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework  import status
from .serializers import AdminFaceEnrollSerializer,MarkAttendanceSerializer,AttendanceSerializer,AttendanceRequestCreateSerializer,AttentanceRequestViewSerializer,AttentanceRequestActionSeriolaizer,AttendanceViewSerializer
from rest_framework.exceptions import PermissionDenied
from .utils.face_utils import verify_face
from .utils.location_utils import verify_location
from .services import get_organisation,prossess_attentance,handle_attendance_request_action
from .models import AttendanceRequest,Attendance
from django.db.models import Q
from account.models import User
from django.shortcuts import get_object_or_404
from .serializers import ManualAttendanceUpsertSerializer
from .services import manual_attendance_upsert
from datetime import datetime
from django.db.models import Count

# from organizations.models import Oganisation
# from django.db.models import Exists, OuterRef
# from employee.models import Employee
# from hr.models import HR
# from accountant.models import Accountent
# from teamlead.models import TeamLead




class SetFaceAPIView(APIView):

    def post(self, request):

        if request.user.user_type not in ["ORG_ADMIN","HR"]:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AdminFaceEnrollSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(admin_user=request.user)
            return Response(
                {"message": "Face registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FaceVerfyAPIView(APIView):
#     def post(self,request):
#         serializer=FaceVerifySerializer(data=request.data,context={"user": request.user})
#         if serializer.is_valid():
#             return Response({"verified": True, "message": "Face verified successfully"},status=status.HTTP_200_OK)
#         return Response({"verified": False, "errors": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
def face_verification(user,img):
    if user.user_type == 'EMPLOYEE':
        if not user.employee.face_encode:
            raise PermissionDenied("Face not registered")
        matched=verify_face(user.employee.face_encode,img)
    elif user.user_type == 'TEAM_LEAD':
        if not user.teamlead.face_encode:
            raise PermissionDenied("Face not registered")
        matched=verify_face(user.teamlead.face_encode,img)
    elif user.user_type == 'HR':
        if not user.hr.face_encode:
            raise PermissionDenied("Face not registered")
        matched=verify_face(user.hr.face_encode,img)
    elif user.user_type == 'ACCOUNTANT':
        if not user.accountant.face_encode:
            raise PermissionDenied("Face not registered")
        matched=verify_face(user.accountant.face_encode,img)
    else:
        raise PermissionDenied("Invalid user type")
    if not matched:
        return False
    return True

def conform_location(request,latitude,longitude):
    user=request.user
    if user.user_type not in ['TEAM_LEAD','EMPLOYEE','HR','ACCOUNTANT']:
        raise PermissionDenied("You have no access")
    org=get_organisation(user)
    if not org:
        raise PermissionDenied("You have no access")
    if not org.latitude or not org.longitude:
        raise PermissionDenied("Office location not set")
    matched=verify_location(org.latitude,org.longitude,latitude,longitude)
    if not matched:
        raise PermissionDenied("You are outside 1 KM office range")
    return True
    
    
# class LiveLocationVerification(APIView): #for veryfly location
#     def post(self,request):
#         if request.user.user_type not in ['TEAM_LEAD','EMPLOYEE','HR','ACCOUNTANT']:
#             return Response({"error":"You have no access"},status=status.HTTP_403_FORBIDDEN)
#         serialiser=LiveLocationveryfySerializer(data=request.data,context={"user":request.user})
        
#         if serialiser.is_valid():
#             return Response({"location verification":True},status=status.HTTP_200_OK)
#         return Response({"location verification":False,"error":serialiser.errors},status=status.HTTP_400_BAD_REQUEST)
    
class MarkAttentanceAPIView(APIView):
    def post(self, request):
        serializer = MarkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        face_image = serializer.validated_data['face_image']
        latitude = serializer.validated_data.get('latitude')
        longitude = serializer.validated_data.get('longitude')

        face_verified = face_verification(request.user, face_image)

        location_verified = True
        if request.user.individual_attendance_mode == 'FACE_LOCATION':
            location_verified = conform_location(request, latitude, longitude)

        attendance = prossess_attentance(
            request.user,
            face_verified,
            location_verified
        )

        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_200_OK
        )

class AttentanceRequestAPIView(APIView): #Reqest Create and View
    def post(self,request):
        serializer=AttendanceRequestCreateSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    from django.db.models import Exists, OuterRef

    def get(self, request):
        user = request.user
        org = get_organisation(user)

        if user.user_type in ['ORG_ADMIN', 'HR']:
            data = AttendanceRequest.objects.filter(
                user__in=User.objects.filter(
                    Q(employee__organization=org) |
                    Q(hr__organization=org) |
                    Q(teamlead__organization=org) |
                    Q(accountent__organization=org)   # ✅ fixed spelling
                ),
                status='PENDING'
            ).order_by('-created_at')
        else:
            data = AttendanceRequest.objects.filter(
                user=user
            ).order_by('-created_at')
            
        if not data:
            return Response({"data not available"})
        serializer = AttentanceRequestViewSerializer(data, many=True)
        return Response(serializer.data)

class AttendanceRequestActionAPIView(APIView):
    def patch(self,request,re_id):
        if request.user.user_type not in ['HR','ORG_ADMIN']:
            return Response({'error':'You are not allowed to approve/reject this request'},status=status.HTTP_403_FORBIDDEN)
        serializer=AttentanceRequestActionSeriolaizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action=serializer.validated_data['action']
        day_type=serializer.validated_data.get('day_type')
        
        attentance_request=get_object_or_404(
            AttendanceRequest,
            id=re_id,
            status='PENDING'
        )
        
        if not attentance_request:
            return Response({"detail": "Attendance request not found or already processed"},status=status.HTTP_404_NOT_FOUND)
        update_request=handle_attendance_request_action(attentance_request,request.user,action,day_type)
        return Response(AttentanceRequestViewSerializer(update_request).data,status=status.HTTP_200_OK)


class ManualAttendanceUpsertAPIView(APIView):

    def patch(self, request):
        serializer = ManualAttendanceUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_user = get_object_or_404(
            User,
            employee_id=serializer.validated_data['employee_id']
        )

        attendance, created = manual_attendance_upsert(
            editor=request.user,
            target_user=target_user,
            date=serializer.validated_data['date'],
            status=serializer.validated_data['status']
        )

        return Response(
            {
                "message": "Attendance created" if created else "Attendance updated",
                "user": attendance.user.email,
                "date": attendance.date,
                "status": attendance.status,
                "marked_by": request.user.email
            },
            status=status.HTTP_200_OK
        )
        
        


class AttendanceViewAPI(APIView):

    def get(self, request):

        employee_id = request.GET.get("employee_id")
        month = request.GET.get("month")  
        user = request.user

        org = get_organisation(user)

        
        if user.user_type in ["ORG_ADMIN", "HR"]:
            
            if employee_id:
                try:
                    target_user = User.objects.get(employee_id=employee_id)
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=404)

            else:
                # HR viewing own attendance
                target_user = user

        # ---------- NORMAL USERS ----------
        else:
            target_user = user


        # ---------- FILTER ATTENDANCE ----------
        records = Attendance.objects.filter(user=target_user)

        if month:
            try:
                year, mon = month.split("-")
                records = records.filter(
                    date__year=year,
                    date__month=mon
                )
            except:
                return Response({"error": "Invalid month format YYYY-MM"}, status=400)

        records = records.order_by("date")

        serializer = AttendanceViewSerializer(records, many=True)

        summary = records.values("status").annotate(total=Count("id"))

        return Response({
            "viewer": user.name,
            "target_user": target_user.name,
            "employee_id": target_user.employee_id,
            "attendance": serializer.data,
            "summary": summary
        })