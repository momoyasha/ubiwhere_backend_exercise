from api.models.road_segment import RoadSegment
from django.contrib.gis.geos import Point
from api.serializers.road_segment_serializer import RoadSegmentSerializer

import logging

logger = logging.getLogger(__name__)


class RoadSegmentRepository:
    """
    Classe de métodos para interagir com entradas RoadSegment
    da base de dados.
    """

    @staticmethod
    def get_or_create_road_segment(
        lat_start: float,
        long_start: float,
        lat_end: float,
        long_end: float,
        length: float,
    ):
        """
        Retorna o segmento de estrada correspondente às coordenadas fornecidas.
        Se um ainda não existe, ele é criado.
        """
        start_point = Point(long_start, lat_start)
        end_point = Point(long_end, lat_end)

        try:
            road_segment = RoadSegment.objects.get(
                start_point=start_point, end_point=end_point
            )
        except RoadSegment.DoesNotExist:
            road_segment = RoadSegment(
                start_point=start_point, end_point=end_point, length=length
            )
            road_segment.save()
            road_segment.refresh_from_db()

            logger.info(f"Segmento cadastrado: ({road_segment})")
        except Exception as ex:
            logger.error(ex)

        return road_segment

    @staticmethod
    def get_all_road_segments():
        """
        Retorna todos os objetos RoadSegments salvos.
        """
        try:
            road_segment = list(RoadSegment.objects.all())
        except Exception as ex:
            logger.info(ex)
            road_segment = None

        return road_segment

    @staticmethod
    def get_road_segment_by_id(id: int):
        """
        Retorna um objeto RoadSegment a partir do id interno.
        """
        try:
            road_segment = RoadSegment.objects.get(id=id)
        except RoadSegment.DoesNotExist:
            road_segment = None

        return road_segment

    @staticmethod
    def delete_road_segment_by_id(id: int):
        """
        Exclui um objeto RoadSegment da base de dados a partir do id interno.
        """
        status_message = ""
        if not id:
            status_message = "É necessário especificar um id para remoção."
        try:
            road_segment = RoadSegment.objects.get(id=id)
            road_segment.delete()
            status_message = f"Registro de segmento de estrada (id: [{id}]) excluído da base de dados com sucesso."
            logger.info(status_message)
        except RoadSegment.DoesNotExist:
            status_message = f"Registro de segmento de estrada (id: [{id}]) não encontrado na base de dados."

        return status_message

    @staticmethod
    def update_road_segment(id: int, new_data: dict):
        """
        Atualiza informações do segmento de estrada especificado.
        """
        status_message = ""

        try:
            road_segment = RoadSegment.objects.get(id=id)
        except RoadSegment.DoesNotExist:
            status_message = f"Registro de segmento de estrada (id: [{id}]) não encontrado na base de dados."
            logger.info(status_message)
            return status_message

        serializer = RoadSegmentSerializer(
            instance=road_segment, data=new_data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            status_message = (
                f"Registro de segmento de estrada (id: [{id}]) atualizado com sucesso."
            )
        else:
            status_message = f"Erro de validação: {serializer.errors}"

        logger.info(status_message)
        return status_message

    @staticmethod
    def create_road_segment(new_data: dict):
        """
        Cria um novo segmento de estrada a partir dos dados fornecidos.
        """
        status_message = ""

        serializer = RoadSegmentSerializer(data=new_data)

        if serializer.is_valid():
            road_segment = serializer.save()
            status_message = f"Registro de segmento de estrada (id: [{road_segment.id}]) criado com sucesso."
        else:
            status_message = f"Erro de validação: {serializer.errors}"

        logger.error(status_message)
        return status_message
