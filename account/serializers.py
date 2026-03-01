from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from secure_files.servise import get_user_image

class LoginSerialiser(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid User")

        data["user"] = user
        return data
            
        
class UserProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "email", "employee_id","phone","photo"]

    def get_photo(self, obj):
        request = self.context.get("request")
        return get_user_image(obj, request)