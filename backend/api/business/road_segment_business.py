from api.models.road_segment import RoadSegment
from api.repository.speed_measurement_repository import SpeedMeasurementRepository
from api.repository.road_segment_repository import RoadSegmentRepository


class RoadSegmentBusiness:
    """
    Classe de métodos para tratar objetos RoadSegment.
    """

    @staticmethod
    def get_measurements_per_road(road_segment_id: int):
        """
        Dado um id de segmento de estrada, busca a quantidade
        de medições associadas.
        """
        road_segment = RoadSegmentRepository.get_road_segment_by_id(id=road_segment_id)
        count = SpeedMeasurementRepository.get_count_of_measurements_by_road_segment_id(
            road_segment_id=road_segment_id
        )

        return {"road_segment": road_segment, "count_of_speed_measurements": count}
