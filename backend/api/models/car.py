from django.db import models


class Car(models.Model):
    """
    Base de carros cujas informações foram capturadas pelos sensores.
    """

    license_plate = models.CharField(blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
