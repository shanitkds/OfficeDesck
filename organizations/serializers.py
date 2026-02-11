from rest_framework import serializers
from account.models import User
from .models import Oganisation
from org_admin.models import Organisation_admin
import uuid



class OrganisationRegistrationSerialiser(serializers.Serializer):
    org_name=serializers.CharField(max_length=200)
    org_email=serializers.EmailField()
    org_phone=serializers.CharField(max_length=200)
    org_address=serializers.CharField()
    org_registration_number=serializers.CharField(required=False, allow_blank=True)
    
    # Admin fieald
    org_admin_name = serializers.CharField(max_length=50)
    org_admin_email=serializers.EmailField()
    org_admin_password=serializers.CharField(write_only=True)
    
    
    
    def create(self, validated_data):
        
        organisation=Oganisation.objects.create(
            name=validated_data["org_name"],
            email=validated_data["org_email"],
            phone=validated_data["org_phone"],
            address=validated_data["org_address"],
            registration_number=validated_data["org_registration_number"]
        )
        
        admin_employee_id = f"ADM-{uuid.uuid4().hex[:8]}"
        
        user=User.objects.create_user(
            name=validated_data["org_admin_name"],
            email=validated_data["org_admin_email"],
            password=validated_data["org_admin_password"],      
            employee_id=admin_employee_id,
            user_type="ORG_ADMIN",
        )
        
        Organisation_admin.objects.create(
            user=user,
            organization=organisation
        )
        
        return organisation

class SetLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Oganisation
        fields=["latitude","longitude"]
        
    def validate(self,attrs):
        lat=attrs.get("latitude")
        log=attrs.get("longitude")
            
        if not (-90 <= lat <= 90):
            raise serializers.ValidationError("Invalid latitude")

        if not (-180 <= log <= 180):
            raise serializers.ValidationError("Invalid longitude")
            
        return attrs