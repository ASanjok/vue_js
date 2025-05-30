from django.contrib.gis.db import models


class PositionData(models.Model):
    position = models.PointField(geography=True,null=True) 
    altitude = models.FloatField(null=True)
    speed = models.FloatField(null=True)
    track = models.FloatField(null=True)
    rc = models.FloatField(null=True)
    epu = models.FloatField(null=True)
    vepu = models.FloatField(null=True)
    hfomr = models.FloatField(null=True)
    vfomr = models.FloatField(null=True)
    hex_code = models.CharField(unique=True)
    icao_id = models.CharField(max_length=10,null=True)
    call_sign = models.CharField(max_length=20, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['hex_code'], name='indx_hex_code'),
        ]

    def __str__(self):
        return f"{self.hex_code} at * position"



class Place(models.Model):
    place_name = models.CharField(max_length=100,null=True)
    time_received = models.DateTimeField(null=True)
    plane_distance = models.FloatField(blank=True, null=True)
    
    PositionData = models.ForeignKey(PositionData, on_delete=models.DO_NOTHING, related_name="positionData")

    class Meta:
        indexes = [
            models.Index(fields=['place_name'], name='indx_place_name')
        ]

    def __str__(self):
        return f"{self.place_name} ({self.plane_distance} km)"
    


