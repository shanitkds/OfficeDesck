from rest_framework import serializers
from .models import PerformanceResult

class ViewPerformenceSerializer(serializers.ModelSerializer):

    employee_name = serializers.SerializerMethodField()
    employee_id=serializers.SerializerMethodField()
    team_lead_name = serializers.SerializerMethodField()
    team_lead_id=serializers.SerializerMethodField()

    class Meta:
        model = PerformanceResult
        fields = [
            "employee_id",
            "employee_name",
            "team_lead_id",
            "team_lead_name",
            "month",
            "year",
            "attendance_score",
            "task_score",
            "review_score",
            "final_score",
            "performance_level",
            "generated_at",
        ]

    def get_employee_name(self, obj):
        return obj.employee.name if obj.employee else None
    def get_employee_id(self,obj):
        return obj.employee.employee_id if obj.employee else None
    def get_team_lead_name(self, obj):
        return obj.team_lead.name if obj.team_lead else None
    def get_team_lead_id(self, obj):
        return obj.team_lead.employee_id if obj.team_lead else None