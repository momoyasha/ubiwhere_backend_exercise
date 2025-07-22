from django.test import TestCase
from api.models.speed_interval import SpeedInterval
from api.business.speed_interval_business import SpeedIntervalBusiness

import logging

logger = logging.getLogger(__name__)


class SpeedIntervalBusinessTests(TestCase):
    def setUp(self):
        SpeedInterval.objects.create(
            criticality=0, criticality_text="elevada", min_speed=None, max_speed=20
        )
        SpeedInterval.objects.create(
            criticality=1, criticality_text="média", min_speed=20, max_speed=50
        )
        SpeedInterval.objects.create(
            criticality=2, criticality_text="baixa", min_speed=50, max_speed=None
        )

    def test_traffic_status_high(self):
        interval_1 = SpeedIntervalBusiness.check_speed_classification(10)
        self.assertIsNotNone(interval_1)
        self.assertEqual(interval_1.criticality, 0)

        interval_2 = SpeedIntervalBusiness.check_speed_classification(20)
        self.assertIsNotNone(interval_2)
        self.assertEqual(interval_2.criticality, 0)

    def test_traffic_status_medium(self):
        interval_1 = SpeedIntervalBusiness.check_speed_classification(21)
        self.assertIsNotNone(interval_1)
        self.assertEqual(interval_1.criticality, 1)

        interval_2 = SpeedIntervalBusiness.check_speed_classification(50)
        self.assertIsNotNone(interval_2)
        self.assertEqual(interval_2.criticality, 1)

    def test_traffic_status_low(self):
        interval_1 = SpeedIntervalBusiness.check_speed_classification(51)
        self.assertIsNotNone(interval_1)
        self.assertEqual(interval_1.criticality, 2)

        interval_2 = SpeedIntervalBusiness.check_speed_classification(80)
        self.assertIsNotNone(interval_2)
        self.assertEqual(interval_2.criticality, 2)
