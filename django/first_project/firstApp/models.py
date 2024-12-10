from django.contrib.gis.db import models
# from django.db import models 
# from django.core.validators import MinValueValidator, MaxValueValidator


# class Anime(models.Model):
#     name = models.CharField(max_length=255)
#     episodeCount = models.IntegerField(default=12)
#     grade = models.IntegerField(default = 0, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     statusF = models.ForeignKey(to='Status', on_delete=models.SET_NULL, default=1, null=True)
#     onEpisode = models.IntegerField(default=0, validators=[MinValueValidator(0)])

#     def __str__(self):
#         return self.name

# class Status(models.Model):
#     name = models.CharField(max_length=10)

#     def __str__(self):
#         return self.name  


class Place(models.Model):
    place_name = models.CharField(max_length=100)
    time_received = models.DateTimeField()
    plane_distance = models.FloatField(blank=True, null=True)
    test_field1 = models.FloatField()
    
    def __str__(self):
        return f"{self.place_name} ({self.plane_distance} km)"


class PositionData(models.Model):
    place = models.ForeignKey(Place, on_delete=models.DO_NOTHING, related_name="positions", null=True, blank=True)

    position = models.PointField(geography=True)  # Для координат (latitude, longitude)
    altitude = models.FloatField()
    speed = models.FloatField()
    track = models.FloatField()
    rc = models.FloatField(blank=True, null=True)
    epu = models.FloatField(blank=True, null=True)
    vepu = models.FloatField(blank=True, null=True)
    hfomr = models.FloatField(blank=True, null=True)
    vfomr = models.FloatField(blank=True, null=True)
    hex_code = models.CharField(blank=True, null=True)
    icao_id = models.CharField(max_length=10, unique=True)
    call_sign = models.CharField(max_length=20, blank=True, null=True)
    test_field2 = models.FloatField()
    test = models.CharField()

    
    def __str__(self):
        return f"{self.hex_code} at * position"
