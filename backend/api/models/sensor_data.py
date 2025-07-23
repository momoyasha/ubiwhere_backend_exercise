from django.db import models

from api.models.road_segment import RoadSegment
from api.models.car import Car
from api.models.sensor import Sensor


class SensorData(models.Model):
    """
    Dados enviados pelos sensores.
    """

    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
