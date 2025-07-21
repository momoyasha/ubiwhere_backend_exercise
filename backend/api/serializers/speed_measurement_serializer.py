from rest_framework import serializers
from rest_framework_gis.fields import GeometryField


class SpeedMeasurementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start_point = GeometryField()
    end_point = GeometryField()
    length = serializers.FloatField()
    speed = serializers.FloatField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
