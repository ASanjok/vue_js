# serializers.py
from rest_framework import serializers
from .models import PositionData

class PositionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionData
        fields = '__all__'  # Укажите поля, которые хотите вернуть в API

class PreviousePositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionData
        fields = ['position']