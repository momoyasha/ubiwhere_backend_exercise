from rest_framework import serializers
from rest_framework_gis.fields import GeometryField


class RoadSegmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start_point = GeometryField()
    end_point = GeometryField()
    length = serializers.FloatField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def update(self, instance, validated_data):
        instance.start_point = validated_data.get("start_point", instance.start_point)
        instance.end_point = validated_data.get("end_point", instance.end_point)
        instance.length = validated_data.get("length", instance.length)
        instance.save()
        return instance
