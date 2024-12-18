from rest_framework import serializers

from .models import PositionData, Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['place_name','time_received','plane_distance','test_field1']

class FlightSerializerGetAll(serializers.ModelSerializer):
    place = PlaceSerializer()

    class Meta:
        model = PositionData
        fields = ['hex_code','position','place','altitude','speed','track','rc','epu','vepu','hfomr','vfomr','icao_id','call_sign','test_field2','test']