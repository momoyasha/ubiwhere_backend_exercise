from api.models.speed_measurement import SpeedMeasurement
import csv
from django.conf import settings
from django.contrib.gis.geos import Point
from api.repository.road_segment_repository import RoadSegmentRepository

import logging

logger = logging.getLogger(__name__)


class SpeedMeasurementBusiness:
    """
    Classe de métodos para tratar objetos SpeedMeasurement.
    """

    def populate_database_with_initial_data():
        """
        Carga inicial na base de dados a partir do csv fornecido no exercício.
        """
        data_points = []

        file_path = settings.BASE_DIR / "data" / "traffic_speed.csv"

        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                road_segment = RoadSegmentRepository.get_or_create_road_segment(
                    lat_start=float(row["Lat_start"]),
                    long_start=float(row["Long_start"]),
                    lat_end=float(row["Lat_end"]),
                    long_end=float(row["Long_end"]),
                    length=float(row["Length"]),
                )
                obj = SpeedMeasurement(
                    measurement_id=row["ID"],
                    road_segment=road_segment,
                    speed=float(row["Speed"]),
                )

                data_points.append(obj)

            try:
                SpeedMeasurement.objects.bulk_create(data_points)
            except Exception as ex:
                logger.info(ex)
