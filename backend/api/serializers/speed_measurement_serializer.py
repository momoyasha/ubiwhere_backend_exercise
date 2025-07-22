from rest_framework import serializers
from rest_framework_gis.fields import GeometryField


class RoadSegmentSerializer(serializers.Serializer):
    start_point = GeometryField()
    end_point = GeometryField()


class SpeedMeasurementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    measurement_id = serializers.IntegerField()
    road_segment = RoadSegmentSerializer()
    speed = serializers.FloatField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
