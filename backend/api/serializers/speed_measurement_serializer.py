from rest_framework import serializers
from rest_framework_gis.fields import GeometryField


class RoadSegmentSerializer(serializers.Serializer):
    start_point = GeometryField()
    end_point = GeometryField()


class TrafficIntensitySerializer(serializers.Serializer):
    criticality = serializers.CharField()
    criticality_text = serializers.CharField()


class SpeedMeasurementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    measurement_id = serializers.IntegerField()
    road_segment = RoadSegmentSerializer()
    speed = serializers.FloatField()
    traffic_intensity = TrafficIntensitySerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
