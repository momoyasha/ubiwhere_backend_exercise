from django.test import TestCase
from rest_framework.exceptions import ValidationError
from api.models.road_segment import RoadSegment
from api.serializers.road_segment_serializer import RoadSegmentSerializer
from django.contrib.gis.geos import Point


class RoadSegmentSerializerTests(TestCase):
    def setUp(self):
        # Para dar update em cima
        self.road_segment_obj = RoadSegment.objects.create(
            start_point=Point(0, 0),
            end_point=Point(1, 1),
            length=1.414,
        )

        # para simular criação via post
        self.valid_data = {
            "start_point": Point(0, 0),
            "end_point": Point(2, 2),
            "length": 1.414,
        }

    def test_create_serializer(self):
        serializer = RoadSegmentSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        new_obj = serializer.save()
        self.assertIsInstance(new_obj, RoadSegment)
        self.assertEqual(new_obj.length, 1.414)

    def test_update_serializer(self):
        serializer = RoadSegmentSerializer(
            instance=self.road_segment_obj, data={"length": 2.0}, partial=True
        )
        self.assertTrue(serializer.is_valid())
        new_obj = serializer.save()
        self.assertEqual(new_obj.length, 2.0)

    def test_missing_required_field(self):
        data = {
            "start_point": Point(0, 0),
            "end_point": Point(2, 2),
        }
        serializer = RoadSegmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("length", serializer.errors)
