from django.test import TestCase
from api.models.road_segment import RoadSegment
from api.models.speed_measurement import SpeedMeasurement
from django.contrib.gis.geos import Point
from api.repository.road_segment_repository import RoadSegmentRepository

import logging

logger = logging.getLogger(__name__)


class SpeedIntervalBusinessTests(TestCase):

    def test_speed_measurement_count(self):
        start_point = Point(45, 45)
        end_point = Point(46, 46)

        road_segment_obj = RoadSegment.objects.create(
            start_point=start_point, end_point=end_point, length=20
        )

        SpeedMeasurement.objects.create(
            measurement_id=1,
            road_segment=road_segment_obj,
            speed=float(30),
        )
        SpeedMeasurement.objects.create(
            measurement_id=2,
            road_segment=road_segment_obj,
            speed=float(25),
        )
        SpeedMeasurement.objects.create(
            measurement_id=3,
            road_segment=road_segment_obj,
            speed=float(26),
        )
        SpeedMeasurement.objects.create(
            measurement_id=4,
            road_segment=road_segment_obj,
            speed=float(40),
        )

        data = RoadSegmentRepository.get_speed_measurements_per_road()
        self.assertEqual(data[0]["speed_measurement_count"], 4)
