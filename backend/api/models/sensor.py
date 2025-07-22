from django.db import models


class Sensor(models.Model):
    """
    Sensores de medição.
    """

    sensor_id = models.IntegerField(blank=False, null=False)
    name = models.CharField(blank=False, null=False)
    uuid = models.CharField(blank=False, null=False)
