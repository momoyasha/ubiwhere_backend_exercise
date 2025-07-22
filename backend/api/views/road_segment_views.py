from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny
from api.repository.road_segment_repository import RoadSegmentRepository
from api.serializers.road_segment_serializer import RoadSegmentSerializer


class RoadSegmentViewSet(ViewSet):
    """
    Viewset de instâncias de medida de velocidade média.

    <expandir a documentação>
    """

    http_method_names = ["get"]
    permission_classes = [AllowAny]

    def list(self, request):
        data = RoadSegmentRepository.get_all_road_segments()
        return Response(
            RoadSegmentSerializer(data, many=True).data, status=status.HTTP_200_OK
        )

    def retrieve(self, request, pk):
        data = RoadSegmentRepository.get_road_segment_by_id(id=pk)
        return Response(RoadSegmentSerializer(data).data, status=status.HTTP_200_OK)
