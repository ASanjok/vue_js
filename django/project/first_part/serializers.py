from rest_framework import serializers
from .models import PositionData

# Full serializer for PositionData
class PositionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionData
        fields = '__all__'  # Include all model fields


# Serializer to return only position field (used for history queries)
class PreviousePositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionData
        fields = ['position']
