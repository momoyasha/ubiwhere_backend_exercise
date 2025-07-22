from rest_framework.response import Response
from rest_framework import status
from api.serializers.speed_measurement_serializer import SpeedMeasurementSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from api.repository.speed_measurement_repository import SpeedMeasurementRepository


class SpeedMeasurementViewSet(ViewSet):
    """
    Viewset de instâncias de medida de velocidade média.

    <expandir a documentação>
    """

    http_method_names = ["get", "put", "patch", "delete"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request):
        data = SpeedMeasurementRepository.get_all_speed_measurements()
        return Response(
            SpeedMeasurementSerializer(data, many=True).data, status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk):
        data = SpeedMeasurementRepository.get_speed_measurement_by_id(id=pk)
        return Response(
            SpeedMeasurementSerializer(data).data, status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        response = SpeedMeasurementRepository.delete_speed_measurement_by_id(id=pk)
        return Response({"status": response}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        pass
