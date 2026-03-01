from rest_framework import serializers
from .models import TaskAssignment
from employee.models import Employee
from django.utils.timezone import now
from attendance.services import get_organisation


class TasckCreationSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    title = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=200, required=False, allow_null=True)
    team_lead_file = serializers.FileField(required=False)
    last_submission_date = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        if user.user_type != "TEAM_LEAD":
            raise serializers.ValidationError(
                "You are not authorized to perform this action"
            )

        team_lead = user.teamlead
        organisation = get_organisation(user)   

        employee = Employee.objects.get(
            id=validated_data["employee_id"],
            team_lead=team_lead
        )

        task = TaskAssignment.objects.create(
            organisation = organisation,        
            title = validated_data["title"],
            description = validated_data.get("description"),
            team_lead = team_lead,
            employee = employee,
            team_lead_file = validated_data.get("team_lead_file"),
            last_submission_date = validated_data.get("last_submission_date"),
            created_at = now()
        )

        return task
    
class TaskViewSerializer(serializers.ModelSerializer):
    team_lead_name = serializers.CharField(source="team_lead.user.name")
    employee_name = serializers.CharField(source="employee.user.name")
    team_lead_file = serializers.SerializerMethodField()
    employee_file = serializers.SerializerMethodField()
    class Meta:
        model=TaskAssignment
        fields=["id","title","organisation","description","team_lead_name","employee_name","team_lead_file","employee_file","team_lead_replay_note","employee_replay_note","status","created_at","submission_date","last_submission_date"]
    def get_team_lead_file(self, obj):
        return obj.team_lead_file.url if obj.team_lead_file else None

    def get_employee_file(self, obj):
        return obj.employee_file.url if obj.employee_file else None
    
from django.utils.timezone import now
from rest_framework import serializers

class TaskSubmitSerializer(serializers.Serializer):
    reaplay_note = serializers.CharField(required=False, allow_blank=True)
    replay_file = serializers.FileField(required=False)

    def update(self, instance, validated_data):
        if instance.status == "APPROVED":
            raise serializers.ValidationError("Locked")

        if "reaplay_note" in validated_data:
            instance.employee_replay_note = validated_data.get("reaplay_note")

        if "replay_file" in validated_data:
            instance.employee_file = validated_data.get("replay_file")

        if not instance.submission_date:
            instance.submission_date = now()

        if instance.status == "ASSIGNED":
            instance.status = "SUBMITTED"
        else:
            instance.status = "RESUBMITTED"

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

        if instance.status not in ["SUBMITTED", "RESUBMITTED"]:
            raise serializers.ValidationError(
                "Only submitted tasks can be reviewed"
            )

        instance.status = validated_data["action"]

        if "review_note" in validated_data:
            instance.team_lead_replay_note = validated_data["review_note"]

        instance.save()
        return instance
