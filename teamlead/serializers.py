from rest_framework import serializers
from .models import TeamLead,TeamLeadReview
from employee.models import Employee


class TeamLeadSerialise(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name")
    email = serializers.CharField(source="user.email")
    employeez_id = serializers.CharField(source="user.employee_id")
    pone = serializers.CharField(source="user.phone")

    photo = serializers.SerializerMethodField()  

    class Meta:
        model = TeamLead
        fields = [
            "id",
            "employeez_id",
            "name",
            "email",
            "pone",
            "desigination",
            "department",
            "photo"
        ]

    def get_photo(self, obj):
        if obj.photo:
            return obj.photo.url
        return None
        
class TeamMembersSerialiser(serializers.ModelSerializer):
    user_id=serializers.IntegerField(source="user.id")
    name = serializers.CharField(source="user.name", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    employeez_id = serializers.CharField(source="user.employee_id", read_only=True)
    pone = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "user_id",
            "employeez_id",
            "name",
            "email",
            "pone",
            "desigination",  
            "department",
        ]

        

class TeamLeadReviewSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source="employee.name",read_only=True)
    employee_id=serializers.CharField(source="employee.employee_id",read_only=True)
    class Meta:
        model=TeamLeadReview
        fields = ["employee","name","employee_id","rating","comment","review_month",]
