from django.contrib.gis.db import models

# Model to store plane position data
class PositionData(models.Model):
    position = models.PointField(geography=True, null=True)  # Geographic point (longitude, latitude)
    altitude = models.FloatField(null=True)
    speed = models.FloatField(null=True)
    track = models.FloatField(null=True)  # Direction of travel in degrees
    rc = models.FloatField(null=True)     # Rate of climb/descent
    epu = models.FloatField(null=True)    # Estimated position uncertainty (horizontal)
    vepu = models.FloatField(null=True)   # Vertical estimated position uncertainty
    hfomr = models.FloatField(null=True)  # Horizontal figure of merit
    vfomr = models.FloatField(null=True)  # Vertical figure of merit
    hex_code = models.CharField(unique=True)  # Unique identifier (Mode S code)
    icao_id = models.CharField(max_length=10, null=True)  # ICAO aircraft identifier
    call_sign = models.CharField(max_length=20, null=True)  # Flight call sign

    class Meta:
        indexes = [
            models.Index(fields=['hex_code'], name='indx_hex_code'),
        ]

    def __str__(self):
        return f"{self.hex_code} at * position"


# Model to store information about a named location and related aircraft distance
class Place(models.Model):
    place_name = models.CharField(max_length=100, null=True)  # Human-readable location name
    time_received = models.DateTimeField(null=True)           # Timestamp when data was received
    plane_distance = models.FloatField(blank=True, null=True) # Distance from the plane in km
    
    PositionData = models.ForeignKey(PositionData, on_delete=models.DO_NOTHING, related_name="positionData")

    class Meta:
        indexes = [
            models.Index(fields=['place_name'], name='indx_place_name')
        ]

    def __str__(self):
        return f"{self.place_name} ({self.plane_distance} km)"
