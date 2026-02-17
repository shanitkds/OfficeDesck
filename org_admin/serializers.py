from rest_framework import serializers
from account.models import User
from accountant.models import Accountent
from hr.models import HR
from teamlead.models import TeamLead
from employee.models import Employee
import uuid
from attendance.services import get_organisation


class OrgAdminCreatUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    user_type=serializers.ChoiceField(
        choices=["TEAM_LEAD","EMPLOYEE","HR","ACCOUNTANT",'ORG_ADMIN']
    )
    phone=serializers.CharField()
    attendance_mode=serializers.ChoiceField(
        ['FACE_ONLY','FACE_LOCATION']
    )
    photo = serializers.ImageField(required=False)
    # induvigal table
    department=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    desigination=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    id_proof = serializers.FileField(required=False)
    attendance_mode=serializers.CharField()
    
    
    
    
    def create(self, validated_data):
        employee_id = f"{validated_data['user_type'][:2]}-{uuid.uuid4().hex[:6]}"
        request=self.context.get("request")
        or_admin=request.user   
        organisation=or_admin.organisation_admin.organization
        
        
        
        user=User.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
            employee_id=employee_id,
            user_type=validated_data["user_type"],
            phone=validated_data["phone"],
            individual_attendance_mode=validated_data['attendance_mode']
        )
        
        if user.user_type=="EMPLOYEE":
            Employee.objects.create(
                user=user,
                organization=organisation,
                photo=validated_data.get('photo'),
                id_proof=validated_data.get('id_proof'),
                department=validated_data["department"],
                desigination=validated_data["desigination"]
            )
        elif user.user_type=="TEAM_LEAD":
            TeamLead.objects.create(
                user=user,
                organization=organisation,
                photo=validated_data.get('photo'),
                id_proof=validated_data.get('id_proof'),
                department=validated_data["department"],
                desigination=validated_data["desigination"]
            )
        elif user.user_type=="HR":
            HR.objects.create(
                user=user,
                organization=organisation,
                photo=validated_data.get('photo'),
                id_proof=validated_data.get('id_proof'),
                department=validated_data["department"],
                desigination=validated_data["desigination"]
            )
        elif user.user_type=="ACCOUNTANT":
            Accountent.objects.create(
                user=user,
                organization=organisation,
                photo=validated_data.get('photo'),
                id_proof=validated_data.get('id_proof'),
                department=validated_data["department"],
                desigination=validated_data["desigination"]
            )
        return user
    
class AssineEmployToTeamleadSerializer(serializers.Serializer):
    employee_id=serializers.IntegerField()
    teamlead_id=serializers.IntegerField()
    
    def create(self, validated_data):
        request=self.context.get("request")
        or_admin=request.user   
        organisation=get_organisation(or_admin)
        
        try:
            employee = Employee.objects.get(
                id=validated_data["employee_id"],
                organization=organisation
            )
        except Employee.DoesNotExist:
            raise serializers.ValidationError(
                {"employee_id": "Employee not found in this organisation"}
            )

        try:
            teamlead = TeamLead.objects.get(
                id=validated_data["teamlead_id"],
                organization=organisation
            )
        except TeamLead.DoesNotExist:
            raise serializers.ValidationError(
                {"teamlead_id": "TeamLead not found in this organisation"}
            )
        
        employee.team_lead=teamlead
        employee.save()
        return employee
    
class OrgAdminUserListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    desigination = serializers.SerializerMethodField()
    id_proof = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()

    attendance_mode_display = serializers.CharField(
        source="get_individual_attendance_mode_display",
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "employee_id",
            "user_type",
            "phone",
            "individual_attendance_mode",
            "attendance_mode_display",
            "image",
            "department",
            "desigination",
            "id_proof",
            "profile_id"
        ]

    # ---------- GET PROFILE ----------
    def get_profile(self, obj):
        if obj.user_type == "EMPLOYEE" and hasattr(obj, "employee"):
            return obj.employee
        if obj.user_type == "TEAM_LEAD" and hasattr(obj, "teamlead"):
            return obj.teamlead
        if obj.user_type == "HR" and hasattr(obj, "hr"):
            return obj.hr
        if obj.user_type == "ACCOUNTENT" and hasattr(obj, "accountent"):
            return obj.accountent
        return None

    def get_image(self, obj):
        profile = self.get_profile(obj)
        request = self.context.get("request")

        if profile and getattr(profile, "photo", None):
            url = profile.photo.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_department(self, obj):
        profile = self.get_profile(obj)
        return getattr(profile, "department", None)

    def get_desigination(self, obj):
        profile = self.get_profile(obj)
        return getattr(profile, "desigination", None)

    def get_id_proof(self, obj):
        profile = self.get_profile(obj)
        request = self.context.get("request")

        if profile and getattr(profile, "id_proof", None):
            url = profile.id_proof.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_profile_id(self, obj):
        profile = self.get_profile(obj)
        return profile.id if profile else None
