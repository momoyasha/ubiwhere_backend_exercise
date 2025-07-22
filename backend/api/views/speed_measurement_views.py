from rest_framework.response import Response
from rest_framework import status
from api.serializers.speed_measurement_serializer import SpeedMeasurementReadSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from api.repository.speed_measurement_repository import SpeedMeasurementRepository


class SpeedMeasurementViewSet(ViewSet):
    """
    Viewset de instâncias de medida de velocidade média.

    <expandir a documentação>
    """

    http_method_names = ["post", "get", "put", "delete"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request):
        data = SpeedMeasurementRepository.get_all_speed_measurements()
        return Response(
            SpeedMeasurementReadSerializer(data, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk):
        data = SpeedMeasurementRepository.get_speed_measurement_by_id(id=pk)
        return Response(
            SpeedMeasurementReadSerializer(data).data, status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        response = SpeedMeasurementRepository.delete_speed_measurement_by_id(id=pk)
        return Response({"status": response}, status=status.HTTP_200_OK)

    def update(self, request, pk):
        response = SpeedMeasurementRepository.update_speed_measurement(
            id=pk, new_data=request.data
        )
        return Response({"status": response}, status=status.HTTP_200_OK)

    def create(self, request):
        response = SpeedMeasurementRepository.create_speed_measurement(
            new_data=request.data
        )
        return Response({"status": response}, status=status.HTTP_200_OK)
