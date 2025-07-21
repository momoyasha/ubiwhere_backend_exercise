from django.db import models
from django.db.models import Q, CheckConstraint


class SpeedInterval(models.Model):
    """
    Intervalos para classificação de velocidade média.
    É necessário que pelo menos um entre max_speed e min_speed
    seja não-nulo.
    """

    # id = models.AutoField(primary_key=True)
    criticality = models.IntegerField(blank=False, null=False, unique=True)
    updated_at = models.DateTimeField(blank=False, null=False, auto_now=True)
    min_speed = models.FloatField(blank=True, null=True)
    max_speed = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} (nível {self.criticality})"

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(min_speed__isnull=False) | Q(max_speed__isnull=False),
                name="at_least_one_speed_not_null",
            )
        ]
