from rest_framework import serializers
from .models import Anime, Status

from .models import Flight, Plane, Place, PositionData

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id','name']

class AnimeSerializerGetAll(serializers.ModelSerializer):
    statusF = StatusSerializer()

    class Meta:
        model = Anime
        fields = ['id', 'name', 'episodeCount', 'statusF', 'onEpisode']

class AnimeSerializerPostNameEpisode(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['name', 'episodeCount']




class PlaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plane
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    plane = PlaneSerializer()

    class Meta:
        model = Flight
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class PositionDataSerializer(serializers.ModelSerializer):
    flight = FlightSerializer()
    place = PlaceSerializer()
    
    class Meta:
        model = PositionData
        fields = '__all__'  # todo: maybe change way how data is structured JSON