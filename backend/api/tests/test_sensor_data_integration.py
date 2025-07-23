from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils.timezone import now
from api.models.sensor import Sensor
from api.models.road_segment import RoadSegment
from django.contrib.gis.geos import Point
from django.conf import settings


class SensorDataViewSetTest(APITestCase):
    def setUp(self):
        self.url = reverse("sensor_data-list")
        self.sensor = Sensor.objects.create(
            name="Sensor 1", uuid="123e4567-e89b-12d3-a456-426614174000", sensor_id=1
        )
        self.road_segment = RoadSegment.objects.create(
            start_point=Point(0, 0), end_point=Point(1, 1), length=100.0
        )
        self.valid_payload = [
            {
                "road_segment": self.road_segment.id,
                "car__license_plate": "AA00AA",
                "timestamp": now().isoformat(),
                "sensor__uuid": str(self.sensor.uuid),
            }
        ]
        self.headers = {"HTTP_X_API_KEY": settings.SENSOR_API_KEY}

    def test_reject_without_api_key(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reject_with_invalid_api_key(self):
        response = self.client.post(
            self.url, self.valid_payload, format="json", HTTP_X_API_KEY="wrong-key"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_accept_with_valid_api_key(self):
        response = self.client.post(
            self.url, self.valid_payload, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reject_invalid_data(self):
        invalid_payload = [
            {
                "road_segment": 999,
                "car__license_plate": "",
                "timestamp": "not-a-date",
                "sensor__uuid": "invalid-uuid",
            }
        ]
        response = self.client.post(
            self.url, invalid_payload, format="json", **self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
