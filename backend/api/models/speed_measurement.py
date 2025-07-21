from django.db import models
from django.contrib.gis.db.models import PointField


class SpeedMeasurement(models.Model):
    """
    Instância de medição de velocidade média.
    """

    measurement_id = models.IntegerField(null=False, blank=False, unique=True)
    start_point = PointField(null=False, blank=False)
    end_point = PointField(null=False, blank=False)
    length = models.FloatField(null=False, blank=False)
    speed = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    updated_at = models.DateTimeField(blank=False, null=False, auto_now=True)
