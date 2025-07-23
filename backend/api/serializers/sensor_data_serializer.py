from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from api.models.road_segment import RoadSegment
from api.models.car import Car
from api.models.sensor import Sensor
from api.models.sensor_data import SensorData
from api.serializers.speed_measurement_serializer import RoadSegmentSerializer


class SensorDataSerializer(serializers.Serializer):
    road_segment = serializers.IntegerField()
    car__license_plate = serializers.CharField()
    timestamp = serializers.DateTimeField()
    sensor__uuid = serializers.UUIDField()

    def create(self, validated_data):
        license_plate = validated_data.pop("car__license_plate")
        sensor_uuid = validated_data.pop("sensor__uuid")
        road_segment_id = validated_data.pop("road_segment")

        car, _ = Car.objects.get_or_create(license_plate=license_plate)

        # "Assume-se que todos os sensores estão previamente registados na base de dados"
        try:
            sensor = Sensor.objects.get(uuid=sensor_uuid)
        except Sensor.DoesNotExist:
            raise serializers.ValidationError(f"Sensor {sensor_uuid} não encontrado")

        try:
            road_segment = RoadSegment.objects.get(id=road_segment_id)
        except RoadSegment.DoesNotExist:
            raise serializers.ValidationError(
                f"Segmento {road_segment_id} não encontrado"
            )

        return SensorData.objects.create(
            car=car,
            sensor=sensor,
            road_segment=road_segment,
            **validated_data,
        )


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    license_plate = serializers.CharField()
    created_at = serializers.DateTimeField()


class SensorDataSensorSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    name = serializers.CharField()


class SensorDataSerializer(serializers.Serializer):
    road_segment = RoadSegmentSerializer()
    timestamp = serializers.DateTimeField()
    sensor = SensorDataSensorSerializer()


class SensorDataByCarSerializer(serializers.Serializer):
    car = CarSerializer()
    sensor_data = SensorDataSerializer(many=True)
