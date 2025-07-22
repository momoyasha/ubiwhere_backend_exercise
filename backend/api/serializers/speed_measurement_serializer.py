from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from api.models.road_segment import RoadSegment
from api.models.speed_measurement import SpeedMeasurement


class RoadSegmentSerializer(serializers.Serializer):
    start_point = GeometryField()
    end_point = GeometryField()


class TrafficIntensitySerializer(serializers.Serializer):
    criticality = serializers.CharField()
    criticality_text = serializers.CharField()


class SpeedMeasurementReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    measurement_id = serializers.IntegerField()
    road_segment = RoadSegmentSerializer()
    speed = serializers.FloatField()
    traffic_intensity = TrafficIntensitySerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class SpeedMeasurementWriteSerializer(serializers.Serializer):
    measurement_id = serializers.IntegerField(
        required=False, default=None, allow_null=True
    )
    speed = serializers.FloatField()

    # conecta o id fornecido no post com um objeto RoadSegment existente
    road_segment = serializers.PrimaryKeyRelatedField(
        queryset=RoadSegment.objects.all()
    )

    def update(self, instance, validated_data):
        instance.speed = validated_data.get("speed", instance.speed)
        instance.road_segment = validated_data.get(
            "road_segment", instance.road_segment
        )
        instance.save()
        return instance

    def create(self, validated_data):
        return SpeedMeasurement.objects.create(**validated_data)


class StatusResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
