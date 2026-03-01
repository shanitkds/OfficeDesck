from rest_framework import serializers
from .models import EmployeeRequest

from rest_framework import serializers
from .models import EmployeeRequest

from rest_framework import serializers
from .models import EmployeeRequest



class EmployeeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=EmployeeRequest
        fields="__all__"
        read_only_fields = ["status", "requested_by", "created_at"]

class EmployeeRequestSerializerView(serializers.ModelSerializer):

    hr_name = serializers.CharField(
        source="requested_by.name",
        read_only=True
    )
    
    

    class Meta:
        model = EmployeeRequest
        fields = [
            "id",
            "hr_name",
            "name",
            "employee_id",
            "email",
            "password",
            "user_type",
            "attendance_mode",
            "department",
            "designation",
            "phone",
            "photo",
            "id_proof",
            "action",
            "status",
            "created_at",
        ]
        read_only_fields = ["status", "requested_by", "created_at"]
