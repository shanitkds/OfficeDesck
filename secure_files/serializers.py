from rest_framework import serializers
from .models import FileShare

class ShareFileSerialiser(serializers.Serializer):
    shared_with =serializers.IntegerField()
    message=serializers.CharField(required=False, allow_blank=True)
    can_view = serializers.BooleanField(default=True)
    can_download = serializers.BooleanField(default=False)