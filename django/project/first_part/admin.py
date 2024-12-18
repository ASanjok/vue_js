from django.contrib import admin

from .models import PositionData, Place

admin.site.register(Place)
admin.site.register(PositionData)