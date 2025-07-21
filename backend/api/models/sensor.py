from django.db import models


class Sensor(models.Model):
    """
    Sensores de medição.
    """

    sensor_id = models.IntegerField(blank=False, null=False)
    name = models.TextField(blank=False, null=False)
    uuid = models.TextField(blank=False, null=False)
