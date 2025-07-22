from django.contrib import admin
from api.models.road_segment import RoadSegment
from api.models.speed_interval import SpeedInterval
from api.models.speed_measurement import SpeedMeasurement

admin.site.register(RoadSegment)
admin.site.register(SpeedMeasurement)
admin.site.register(SpeedInterval)
