from rest_framework import serializers
from .models import FileShare,SecureFile

class ShareFileSerialiser(serializers.Serializer):
    shared_with =serializers.IntegerField()
    message=serializers.CharField(required=False, allow_blank=True)
    can_view = serializers.BooleanField(default=True)
    can_download = serializers.BooleanField(default=False)
    

class SecureFileSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.name", read_only=True)

    owner_employee_id = serializers.CharField(
        source="owner.employee_id",
        read_only=True,
        default=""
    )

    file_url = serializers.SerializerMethodField()

    class Meta:
        model = SecureFile
        fields = [
            "id",
            "original_name",
            "file_type",
            "mime_type",
            "owner_name",
            "owner_employee_id",
            "file_url",
            "created_at",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.encrypted_file:
            return request.build_absolute_uri(obj.encrypted_file.url)
        return None

    
    
class ShareHistorySerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(source="file.original_name")
    shared_from = serializers.CharField(source="shared_by.name")
    shared_from_id = serializers.CharField(source="shared_by.employee_id")
    shared_to = serializers.CharField(source="shared_with.name")
    shared_to_id = serializers.CharField(source="shared_with.employee_id")

    class Meta:
        model = FileShare
        fields = [
            "id",
            "file_name",
            "shared_from",
            "shared_to",
            "shared_from_id",
            "shared_at",
            "shared_to_id"
        ]
    
class SharedWithMeSerializer(serializers.ModelSerializer):

    share_id = serializers.IntegerField(source="id", read_only=True)

    file_id = serializers.IntegerField(source="file.id", read_only=True)
    file_name = serializers.CharField(source="file.original_name", read_only=True)
    file_type = serializers.CharField(source="file.file_type", read_only=True)
    file_url = serializers.SerializerMethodField()

    owner_name = serializers.CharField(source="file.owner.name", read_only=True)
    owner_employee_id = serializers.CharField(
        source="file.owner.employee_id",
        read_only=True,
        allow_null=True
    )

    shared_by_name = serializers.CharField(source="shared_by.name", read_only=True)
    shared_by_employee_id = serializers.CharField(
        source="shared_by.employee_id",
        read_only=True,
        allow_null=True
    )
    

    created_at = serializers.DateTimeField(source="file.created_at", read_only=True)

    class Meta:
        model = FileShare
        fields = [
            "share_id",
            "file_id",
            "file_name",
            "file_type",
            "file_url",
            "owner_name",
            "owner_employee_id",
            "shared_by_name",
            "shared_by_employee_id",
            "can_view",
            "can_download",
            "created_at",
        ]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file and obj.file.encrypted_file:
            return request.build_absolute_uri(obj.file.encrypted_file.url)
        return None
