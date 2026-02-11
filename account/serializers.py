from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

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
            