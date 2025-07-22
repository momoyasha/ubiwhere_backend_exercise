from api.models.road_segment import RoadSegment
from django.contrib.gis.geos import Point

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
