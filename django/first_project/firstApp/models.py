from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Anime(models.Model):
    name = models.CharField(max_length=255)
    episodeCount = models.IntegerField(default=12)
    grade = models.IntegerField(default = 0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    statusF = models.ForeignKey(to='Status', on_delete=models.SET_NULL, default=1, null=True)
    onEpisode = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
