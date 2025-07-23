from django.test import TestCase
from api.models.road_segment import RoadSegment
from api.models.speed_measurement import SpeedMeasurement
from api.models.speed_interval import SpeedInterval
from api.filters.road_segment_filters import RoadSegmentFilter
from django.utils.timezone import now
from django.contrib.gis.geos import Point

from api.business.speed_interval_business import SpeedIntervalBusiness


class RoadSegmentFilterTest(TestCase):
    def setUp(self):
        self.segment_high = RoadSegment.objects.create(
            start_point=Point(0, 0), end_point=Point(1, 1), length=100.0
        )
        self.segment_low = RoadSegment.objects.create(
            start_point=Point(3, 2), end_point=Point(2, 8), length=200.0
        )

        SpeedMeasurement.objects.create(
            road_segment=self.segment_low,
            speed=80.0,
            created_at=now(),
        )
        SpeedMeasurement.objects.create(
            road_segment=self.segment_high,
            speed=10.0,
            created_at=now(),
        )

        # Criar os intervalos de velocidade
        SpeedInterval.objects.create(
            min_speed=0,
            max_speed=30,
            criticality="0",
            criticality_text="alta",
        )

        SpeedInterval.objects.create(
            min_speed=30,
            max_speed=200,
            criticality="1",
            criticality_text="baixa",
        )

    def test_filter_by_traffic_intensity_high(self):

        queryset = RoadSegment.objects.all()
        filterset = RoadSegmentFilter(
            data={"traffic_intensity": "alta"}, queryset=queryset
        )
        result = filterset.qs

        self.assertIn(self.segment_high, result)
        self.assertNotIn(self.segment_low, result)

    def test_filter_by_traffic_intensity_low(self):
        queryset = RoadSegment.objects.all()
        filterset = RoadSegmentFilter(
            data={"traffic_intensity": "baixa"}, queryset=queryset
        )
        result = filterset.qs

        self.assertIn(self.segment_low, result)
        self.assertNotIn(self.segment_high, result)
