from api.models.speed_measurement import SpeedMeasurement
from api.serializers.speed_measurement_serializer import SpeedMeasurementWriteSerializer


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

    @staticmethod
    def delete_speed_measurement_by_id(id: int):
        """
        Exclui um objeto SpeedMeasurement da base de dados a partir do id interno.
        """
        status_message = ""
        if not id:
            status_message = "É necessário especificar um id para remoção."
        try:
            speed_measurement = SpeedMeasurement.objects.get(id=id)
            speed_measurement.delete()
            status_message = f"Registro de velocidade (id: [{id}]) excluído da base de dados com sucesso."
            logger.info(status_message)
        except SpeedMeasurement.DoesNotExist:
            status_message = (
                f"Registro de velocidade (id: [{id}]) não encontrado na base de dados."
            )

        return status_message

    @staticmethod
    def get_speed_measurements_by_road_segment_id(road_segment_id: int):
        """
        Retorna uma lista de medidas de velocidade para um dado segmento de estrada.
        """
        try:
            speed_measurements = SpeedMeasurement.objects.filter(
                road_segment__id=road_segment_id
            )
        except Exception as ex:
            speed_measurements = []

        return speed_measurements

    @staticmethod
    def update_speed_measurement(id: int, new_data: dict):
        """
        Atualiza informações da medição de velocidade especificada.
        """
        status_message = ""

        try:
            speed_measurement = SpeedMeasurement.objects.get(id=id)
        except SpeedMeasurement.DoesNotExist:
            status_message = f"Registro de medição de velocidade (id: [{id}]) não encontrado na base de dados."
            logger.info(status_message)
            return status_message

        serializer = SpeedMeasurementWriteSerializer(
            instance=speed_measurement, data=new_data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            status_message = f"Registro de medição de velocidade (id: [{id}]) atualizado com sucesso."
        else:
            status_message = f"Erro de validação: {serializer.errors}"

        logger.info(status_message)
        return status_message

    @staticmethod
    def create_speed_measurement(new_data: dict):
        """
        Cria um novo medição de velocidade a partir dos dados fornecidos.
        """
        status_message = ""

        serializer = SpeedMeasurementWriteSerializer(data=new_data)

        if serializer.is_valid():
            speed_measurement = serializer.save()
            status_message = f"Registro de medição de velocidade (id: [{speed_measurement.id}]) criado com sucesso."
        else:
            status_message = f"Erro de validação: {serializer.errors}"

        logger.error(status_message)
        return status_message

    @staticmethod
    def get_count_of_measurements_by_road_segment_id(road_segment_id: int):
        try:
            count = SpeedMeasurement.objects.filter(
                road_segment__id=road_segment_id
            ).count()
        except Exception as ex:
            count = 0

        return count
