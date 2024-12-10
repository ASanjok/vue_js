from rest_framework import serializers

# from .models import Anime, Status

from .models import PositionData, Place

# from .models import Flight, Plane, Place, PositionData

# class StatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Status
#         fields = ['id','name']

# class AnimeSerializerGetAll(serializers.ModelSerializer):
#     statusF = StatusSerializer()

#     class Meta:
#         model = Anime
#         fields = ['id', 'name', 'episodeCount', 'statusF', 'onEpisode']

# class AnimeSerializerPostNameEpisode(serializers.ModelSerializer):
#     class Meta:
#         model = Anime
#         fields = ['name', 'episodeCount']



class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['place_name','time_received','plane_distance','test_field1']

class FlightSerializerGetAll(serializers.ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = PositionData
        fields = ['hex_code','position','place','altitude','speed','track','rc','epu','vepu','hfomr','vfomr','icao_id','call_sign','test_field2','test']

