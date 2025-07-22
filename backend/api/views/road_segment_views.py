from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from api.repository.road_segment_repository import RoadSegmentRepository
from api.serializers.road_segment_serializer import (
    RoadSegmentSerializer,
    MeasurementsPerRoadSegmentSerializer,
)
from rest_framework.views import APIView


class RoadSegmentViewSet(ViewSet):
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
        data = RoadSegmentRepository.get_all_road_segments()
        return Response(
            RoadSegmentSerializer(data, many=True).data, status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk):
        data = RoadSegmentRepository.get_road_segment_by_id(id=pk)
        return Response(RoadSegmentSerializer(data).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        response = RoadSegmentRepository.delete_road_segment_by_id(id=pk)
        return Response({"status": response}, status=status.HTTP_200_OK)

    def update(self, request, pk):
        response = RoadSegmentRepository.update_road_segment(
            id=pk, new_data=request.data
        )
        return Response({"status": response}, status=status.HTTP_200_OK)

    def create(self, request):
        response = RoadSegmentRepository.create_road_segment(new_data=request.data)
        return Response({"status": response}, status=status.HTTP_200_OK)


class RoadSegmentRelatedDataView(APIView):
    """
    Informações de medição de velocidade por segmento de estrada.

    <expandir a documentação>
    """

    http_method_names = ["get"]

    permission_classes = [AllowAny]

    def get(self, request):
        response = RoadSegmentRepository.get_speed_measurements_per_road()
        return Response(
            MeasurementsPerRoadSegmentSerializer(response, many=True).data,
            status=status.HTTP_200_OK,
        )
