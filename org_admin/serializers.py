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
        choices=["TEAM_LEAD","EMPLOYEE","HR","ACCOUNTANT"]
    )
    phone=serializers.CharField(required=False)
    
    # induvigal table
    department=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    desigination=serializers.CharField(required=False,allow_null=True,allow_blank=True)
    
    
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
            phone=validated_data["phone"]
        )
        
        if user.user_type=="EMPLOYEE":
            Employee.objects.create(
                user=user,
                organization=organisation,
                department=validated_data["department"],
                desigination=validated_data["desigination"]
            )
        elif user.user_type=="TEAM_LEAD":
            TeamLead.objects.create(
                user=user,
                organization=organisation,
                department=validated_data["department"],
                desigination=validated_data["desigination"]
            )
        elif user.user_type=="HR":
            HR.objects.create(
                user=user,
                organization=organisation,
                department=validated_data["department"],
                desigination=validated_data["desigination"]
            )
        elif user.user_type=="ACCOUNTANT":
            Accountent.objects.create(
                user=user,
                organization=organisation,
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