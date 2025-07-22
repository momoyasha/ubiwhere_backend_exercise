from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from api.models.road_segment import RoadSegment


class RoadSegmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    start_point = GeometryField()
    end_point = GeometryField()
    length = serializers.FloatField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        instance.start_point = validated_data.get("start_point", instance.start_point)
        instance.end_point = validated_data.get("end_point", instance.end_point)
        instance.length = validated_data.get("length", instance.length)
        instance.save()
        return instance

    def create(self, validated_data):
        return RoadSegment.objects.create(**validated_data)


class MeasurementsPerRoadSegmentSerializer(serializers.Serializer):
    road_id = serializers.IntegerField(source="id")
    count_of_speed_measurements = serializers.IntegerField(
        source="speed_measurement_count"
    )
