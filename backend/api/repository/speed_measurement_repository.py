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

    @staticmethod
    def get_all_speed_measurements():
        """
        Retorna todos os objetos SpeedMeasurements salvos.
        """
        try:
            speed_measurements = list(SpeedMeasurement.objects.all())
        except Exception as ex:
            logger.info(ex)
            speed_measurements = None

        return speed_measurements

    @staticmethod
    def get_speed_measurement_by_id(id: int):
        """
        Retorna um objeto SpeedMeasurement a partir do id interno.
        """
        try:
            speed_measurement = SpeedMeasurement.objects.get(id=id)
        except SpeedMeasurement.DoesNotExist:
            speed_measurement = None

        return speed_measurement
