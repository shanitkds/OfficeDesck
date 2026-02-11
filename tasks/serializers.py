from rest_framework import serializers
from .models import TaskAssignment
from employee.models import Employee
from django.utils.timezone import now



class TasckCreationSerializer(serializers.Serializer):
    employee_id=serializers.CharField()
    title=serializers.CharField(max_length=20,)
    description=serializers.CharField(max_length=200,required=False,allow_null=True)
    team_lead_file=serializers.FileField(required=False)
    last_submission_date=serializers.DateTimeField(required=False)
    def create(self,validated_data):
        request=self.context.get("request")
        user=request.user

        if request.user.user_type != "TEAM_LEAD":
            raise serializers.ValidationError("You are not authorized to perform this action")
        team_lead=user.teamlead
        employee=Employee.objects.get(id=validated_data["employee_id"],team_lead=team_lead)
        task=TaskAssignment.objects.create(
            title=validated_data["title"],
            description=validated_data["description"],
            team_lead=team_lead,
            employee=employee,
            team_lead_file=validated_data.get("team_lead_file"),
            last_submission_date=validated_data.get("last_submission_date"),
            created_at=now() #for check
        )

        return task
class TaskViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=TaskAssignment
        fields="__all__"

class TaskSubmitSerializer(serializers.Serializer):
    reaplay_note=serializers.CharField(required=False,allow_blank=True)
    replay_file=serializers.FileField(required=False)
    def update(self, instance, validated_data):
        if instance.status == "APPROVED":
            raise serializers.ValidationError("Locked")
        instance.employee_file=validated_data.get("replay_file")
        instance.employee_replay_note=validated_data.get("reaplay_note")
        if not instance.submission_date:
            instance.submission_date = now()
        if instance.status=="ASSIGNED":
            instance.status="SUBMITTED"
        else:
            instance.status="RESUBMITTED"
        instance.save()
        return instance

class ApproveSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=["APPROVED", "REJECTED"]
    )
    review_note = serializers.CharField(
        required=False,
        allow_blank=True
    )
    def update(self, instance, validated_data):
        # if instance.status != "SUBMITTED":
        #     raise serializers.ValidationError(
        #         "Only submitted tasks can be reviewed"
        #     )
            
        instance.status=validated_data["action"]
        
        instance.description = validated_data.get("review_note")   
            
        instance.save()
        return instance