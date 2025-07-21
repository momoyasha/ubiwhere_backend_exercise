from api.models.speed_interval import SpeedInterval

import logging

logger = logging.getLogger(__name__)


class SpeedIntervalRepository:
    """
    Classe de métodos para interagir com entradas SpeedInterval
    da base de dados.
    """

    @staticmethod
    def save_speed_interval(criticality: int, min_speed=None, max_speed=None):
        """
        Cadastra ou atualiza um intervalo de velocidade.
        """
        try:
            existing_interval = SpeedInterval.objects.get(criticality=criticality)
        except SpeedInterval.DoesNotExist:
            existing_interval = SpeedInterval(criticality=criticality)

        existing_interval.max_speed = max_speed
        existing_interval.min_speed = min_speed

        try:
            existing_interval.save()
        except Exception as ex:
            logger.error(f"Erro ao salvar intervalo de velocidade - [{ex}]")

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
                not interval.max_speed or speed < interval.max_speed
            ):
                return interval

        return None
