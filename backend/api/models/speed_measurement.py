from django.db import models
from django.contrib.gis.db.models import PointField
from api.models.road_segment import RoadSegment
from api.business.speed_interval_business import SpeedIntervalBusiness


class SpeedMeasurement(models.Model):
    """
    Instância de medição de velocidade média.
    """

    measurement_id = models.IntegerField(null=False, blank=False, unique=True)
    road_segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    speed = models.FloatField(null=False, blank=False)
    created_at = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    updated_at = models.DateTimeField(blank=False, null=False, auto_now=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: road_segment: [{self.road_segment.id}]; speed:[{self.speed}]"

    @property
    def traffic_intensity(self):
        """
        Adiciona dados de intensidade de trânsito
        """

        corresponding_interval = SpeedIntervalBusiness.check_speed_classification(
            self.speed
        )

        if corresponding_interval:
            traffic_intensity = {
                "criticality": corresponding_interval.criticality,
                "criticality_text": corresponding_interval.criticality_text,
            }
        else:
            traffic_intensity = {"criticality": None, "criticality_text": None}

        return traffic_intensity
