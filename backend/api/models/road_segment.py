from django.db import models
from django.contrib.gis.db.models import PointField


class RoadSegment(models.Model):
    """
    Segmentos de estrada. Medições de velocidade são sempre
    associadas a um desses.
    """

    start_point = PointField(null=False, blank=False)
    end_point = PointField(null=False, blank=False)
    length = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    updated_at = models.DateTimeField(blank=False, null=False, auto_now=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} [{self.id}]"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["start_point", "end_point"], name="unique_start_point_end_point"
            )
        ]
