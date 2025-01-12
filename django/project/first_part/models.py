from django.contrib.gis.db import models


class PositionData(models.Model):
    position = models.PointField(geography=True) 
    altitude = models.FloatField()
    speed = models.FloatField(null=True)
    track = models.FloatField()
    rc = models.FloatField(blank=True)
    epu = models.FloatField(blank=True)
    vepu = models.FloatField(blank=True)
    hfomr = models.FloatField(blank=True)
    vfomr = models.FloatField(blank=True)
    hex_code = models.CharField(blank=True, unique=True)
    icao_id = models.CharField(max_length=10)
    call_sign = models.CharField(max_length=20, blank=True, null=True)

    
    def __str__(self):
        return f"{self.hex_code} at * position"



class Place(models.Model):
    place_name = models.CharField(max_length=100)
    time_received = models.DateTimeField()
    plane_distance = models.FloatField(blank=True, null=True)
    
    PositionData = models.ForeignKey(PositionData, on_delete=models.DO_NOTHING, related_name="positionData", blank=True)

    def __str__(self):
        return f"{self.place_name} ({self.plane_distance} km)"



