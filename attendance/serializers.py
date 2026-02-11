from rest_framework import serializers
from .utils.face_utils import get_face_encoding #,verify_face
# from .utils.location_utils import verify_location
from .services import get_today_attentance #,get_organisation
from .models import Attendance,AttendanceRequest


class FaceEntrollSerializer(serializers.Serializer):
    face_image=serializers.ImageField()
    
    def save(self,user):
        if user.user_type=='EMPLOYEE':
            if user.employee.face_encode:
                raise serializers.ValidationError("Face already registered. Contact admin.")
            encode=get_face_encoding(self.validated_data["face_image"])
            user.employee.face_encode=encode
            user.employee.save()
        elif user.user_type=='TEAM_LEAD':
            if user.teamlead.face_encode:
                raise serializers.ValidationError("Face already registered. Contact admin.")
            encode=get_face_encoding(self.validated_data["face_image"])
            user.teamlead.face_encode=encode
            user.teamlead.save()
        elif user.user_type=='HR':
            if user.hr.face_encode:
                raise serializers.ValidationError("Face already registered. Contact admin.")
            encode=get_face_encoding(self.validated_data["face_image"])
            user.hr.face_encode=encode
            user.hr.save()
        elif user.user_type=='ACCOUNTANT':
            if user.accountant.face_encode:
                raise serializers.ValidationError("Face already registered. Contact admin.")
            encode=get_face_encoding(self.validated_data["face_image"])
            user.accountant.face_encode=encode
            user.accountant.save()
        else:
            raise serializers.ValidationError("Invalid user type for face enrollment")
        return user
    
# class FaceVerifySerializer(serializers.Serializer):
#     face_image = serializers.ImageField()

#     def validate(self, attrs):
#         user = self.context.get("user")

#         if user.user_type == 'EMPLOYEE':
#             if not user.employee.face_encode:
#                 raise serializers.ValidationError("Face not registered")

#             try:
#                 matched = verify_face(
#                     user.employee.face_encode,
#                     attrs["face_image"]
#                 )
#             except ValueError as e:
#                 raise serializers.ValidationError(str(e))

#             # ✅ THIS IS MANDATORY
#             if not matched:
#                 raise serializers.ValidationError("Face not matched")

#         return attrs  # ✅ ONLY reached when face is correct

# class LiveLocationveryfySerializer(serializers.Serializer):
#     latitude =serializers.FloatField()
#     longitude =serializers.FloatField()
    
#     def validate(self, attrs):
#         user=self.context.get('user')
        
#         org=get_organisation(user)
#         if not org:
#             raise serializers.ValidationError("Invalid user type")
#         # if user.user_type =="EMPLOYEE":
#         #     org=user.employee.organization
#         # elif user.user_type=="TEAM_LEAD":
#         #     org=user.teamlead.organization
#         # elif user.user_type=="HR":
#         #     org=user.hr.organization
#         # elif user.user_type == "ACCOUNTANT":
#         #     org=user.accountant.organization
#         # else:
#         #     raise serializers.ValidationError("Invalid user type")
        
#         # print("time:::",timezone.localtime().time())
#         if not org.latitude or not org.longitude:
#             raise serializers.ValidationError("Office location not set")
        
#         matched=verify_location(org.latitude,org.longitude,attrs["latitude"],attrs["longitude"],allowed_km=1)
#         # print(matched)
#         if not matched:
#             raise serializers.ValidationError("You are outside 1 KM office range")
#         return attrs
    
class MarkAttendanceSerializer(serializers.Serializer):
    face_image=serializers.ImageField()
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields = '__all__'
        
# attentance request

class AttendanceRequestCreateSerializer(serializers.Serializer):
    reason = serializers.CharField()
    
    def create(self, validated_data):
        user = self.context.get('user')
        attentance=get_today_attentance(user)
        if AttendanceRequest.objects.filter(user=user,attendance=attentance).exists():
            raise serializers.ValidationError("You have already submitted an attendance request for today.")
        attentance_request=AttendanceRequest.objects.create(
            user=user,
            attendance=attentance,
            reason=validated_data["reason"]
        )
        
        return attentance_request
    

class AttentanceRequestViewSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='user.name', read_only=True)
    email= serializers.EmailField(source='user.email', read_only=True)
    attendance_date=serializers.DateField(source='attendance.date', read_only=True)
    class Meta:
        model=AttendanceRequest
        fields=['id','name','email','attendance_date','reason','status','created_at','reviewed_at']
        
        
class AttentanceRequestActionSeriolaizer(serializers.Serializer):
    action=serializers.ChoiceField(choices=['APPROVE', 'REJECT'])
    day_type=serializers.ChoiceField(choices=['FULL_DAY', 'HALF_DAY'],required=False)
    
    def validate(self, attrs):
        if attrs['action']=='APPROVED' and not attrs.get('day_type'):
            raise serializers.ValidationError("day_type is required when approving a request")
        
        return attrs
    
class ManualAttendanceUpsertSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    date = serializers.DateField()
    status = serializers.ChoiceField(
        choices=['FULL_DAY', 'HALF_DAY', 'ABSENT']
    )