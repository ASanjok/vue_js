from rest_framework import serializers
from .models import Anime, Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id','name']

class AnimeSerializerGetAll(serializers.ModelSerializer):
    statusF = StatusSerializer()

    class Meta:
        model = Anime
        fields = ('id', 'name', 'episodeCount', 'statusF', 'onEpisode')

class AnimeSerializerPostNameEpisode(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['name', 'episodeCount']