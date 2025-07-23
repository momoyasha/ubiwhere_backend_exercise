from django.test import TestCase
from rest_framework.exceptions import ValidationError
from api.models.road_segment import RoadSegment
from api.models.speed_measurement import SpeedMeasurement
from api.serializers.speed_measurement_serializer import SpeedMeasurementWriteSerializer
from django.contrib.gis.geos import Point


class SpeedMeasurementSerializerTests(TestCase):
    def setUp(self):
        # Para dar update em cima
        self.road_segment_obj = RoadSegment.objects.create(
            start_point=Point(0, 0),
            end_point=Point(1, 1),
            length=1.414,
        )

        # para simular criação via post
        self.valid_data = {
            "speed": 50.0,
            "road_segment": self.road_segment_obj.id,
        }

    def test_create_valid_measurement(self):
        serializer = SpeedMeasurementWriteSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instancia = serializer.save()
        self.assertIsInstance(instancia, SpeedMeasurement)
        self.assertEqual(instancia.speed, 50.0)

    def test_create_invalid_speed_type(self):
        data = {"speed": "cinquenta", "road_segment": self.road_segment_obj.id}
        serializer = SpeedMeasurementWriteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("speed", serializer.errors)

    def test_create_invalid_road_segment(self):
        data = {"speed": 50.0, "road_segment": 9999}
        serializer = SpeedMeasurementWriteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("road_segment", serializer.errors)

    def test_update_measurement(self):
        existing_measurement = SpeedMeasurement.objects.create(
            speed=30.0, road_segment=self.road_segment_obj
        )
        new_road_segment = RoadSegment.objects.create(
            start_point=Point(2, 2),
            end_point=Point(6, 6),
            length=3.14,
        )
        serializer = SpeedMeasurementWriteSerializer(
            instance=existing_measurement,
            data={"speed": 80.0, "road_segment": new_road_segment.id},
        )
        self.assertTrue(serializer.is_valid())
        instancia = serializer.save()
        self.assertEqual(instancia.speed, 80.0)
        self.assertEqual(instancia.road_segment.id, new_road_segment.id)
