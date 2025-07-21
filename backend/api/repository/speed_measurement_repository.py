from api.models.speed_measurement import SpeedMeasurement


import logging

logger = logging.getLogger(__name__)


class SpeedMeasurementRepository:
    """
    Classe de métodos para interagir com entradas SpeedMeasurement
    da base de dados.
    """

    @staticmethod
    def save_new_speed_measurement(speed_measurement_obj: SpeedMeasurement):
        """
        Salva um novo objeto SpeedMeasurement na base de dados.
        """
        try:
            speed_measurement_obj.save()
            speed_measurement_obj.refresh_from_db()
            return speed_measurement_obj
        except Exception as ex:
            logger.error(f"Erro ao salvar SpeedMeasurement - [{ex}]")
            return None
