from rest_framework import serializers
from organizations.models import Oganisation

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oganisation
        fields = "__all__"
        
