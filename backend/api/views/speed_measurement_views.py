from rest_framework.response import Response
from rest_framework import status
from api.serializers.speed_measurement_serializer import SpeedMeasurementSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from api.repository.speed_measurement_repository import SpeedMeasurementRepository


class SpeedMeasurementViewSet(ViewSet):
    """
    Viewset de instâncias de medida de velocidade média.

    <expandir a documentação>
    """

    http_method_names = ["get"]
    permission_classes = [AllowAny]

    def list(self, request):
        plane = SpeedMeasurementRepository.get_all_speed_measurements()
        return Response(
            SpeedMeasurementSerializer(plane, many=True).data, status=status.HTTP_200_OK
        )

    # def retrieve(self, request, pk):
    #     plane = PlaneRepository.get_plane_by_id(id=pk)
    #     return Response(PlaneSerializer(plane).data, status=status.HTTP_200_OK)
