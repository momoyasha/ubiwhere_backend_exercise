from api.models.speed_interval import SpeedInterval

import logging

logger = logging.getLogger(__name__)


class SpeedIntervalRepository:
    """
    Classe de métodos para interagir com entradas SpeedInterval
    da base de dados.
    """

    @staticmethod
    def save_speed_interval(
        criticality: int, criticality_text: str, min_speed=None, max_speed=None
    ):
        """
        Cadastra ou atualiza um intervalo de velocidade.
        """
        try:
            existing_interval = SpeedInterval.objects.get(
                criticality=criticality, criticality_text=criticality_text
            )
        except SpeedInterval.DoesNotExist:
            existing_interval = SpeedInterval()

        existing_interval.criticality = criticality
        existing_interval.criticality_text = criticality_text
        existing_interval.max_speed = max_speed
        existing_interval.min_speed = min_speed

        try:
            existing_interval.save()
            logger.info(
                f"Intervalo de velocidade (min {min_speed}, max {max_speed}) criado"
            )
        except Exception as ex:
            logger.error(f"Erro ao salvar intervalo de velocidade - [{ex}]")
