from api.models.speed_interval import SpeedInterval
from api.repository.speed_interval_repository import SpeedIntervalRepository

import logging

logger = logging.getLogger(__name__)


class SpeedIntervalBusiness:
    """
    Classe de métodos para tratar objetos SpeedInterval.
    """

    @staticmethod
    def check_speed_classification(speed: float):
        """
        Classifica a velocidade fornecida de acordo com os
        intervalos de velocidade cadastrados.
        """
        speed_intervals = list(SpeedInterval.objects.all())

        for interval in speed_intervals:
            # se a velocidade é maior do que a mínima (se esta existir)
            # e menor do que a máxima (se esta existir)
            if (not interval.min_speed or speed > interval.min_speed) and (
                not interval.max_speed or speed <= interval.max_speed
            ):
                return interval

        return None

    @staticmethod
    def populate_database_with_initial_data():
        """
        Popula a base com intervalos <= 20, >20 <=50, >50
        """
        SpeedIntervalRepository.save_speed_interval(
            criticality=0, criticality_text="elevada", min_speed=None, max_speed=20
        )
        SpeedIntervalRepository.save_speed_interval(
            criticality=1, criticality_text="média", min_speed=20, max_speed=50
        )
        SpeedIntervalRepository.save_speed_interval(
            criticality=2, criticality_text="baixa", min_speed=50, max_speed=None
        )
