from django.db import models


class SpeedInterval(models.Model):
    """
    Intervalos para classificação de velocidade média.
    """

    # id = models.AutoField(primary_key=True)
    criticality = models.IntegerField(null=False, blank=False, unique=True)
    updated_at = models.DateTimeField(blank=False, null=False, auto_now=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} (nível {self.criticality})"
