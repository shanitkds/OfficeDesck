from rest_framework import serializers
from .models import TeamLead,TeamLeadReview
from employee.models import Employee


class TeamLeadSerialise(serializers.ModelSerializer):
    name=serializers.CharField(source="user.name")
    email=serializers.CharField(source="user.email")
    employeez_id=serializers.CharField(source="user.employee_id")
    pone=serializers.CharField(source="user.phone")
    class Meta:
        model=TeamLead
        fields=["employeez_id","name","email","pone","desigination","department",]
        
class TeamMembersSerialiser(serializers.ModelSerializer):
    name=serializers.CharField(source="user.name")
    email=serializers.CharField(source="user.email")
    employeez_id=serializers.CharField(source="user.employee_id")
    pone=serializers.CharField(source="user.phone")
    class Meta:
        model=Employee
        fields=["employeez_id","name","email","pone","desigination","department",]
        

class TeamLeadReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=TeamLeadReview
        fields = ["employee","rating","comment","review_month",]
