from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from api.repository.road_segment_repository import RoadSegmentRepository
from api.serializers.road_segment_serializer import (
    RoadSegmentSerializer,
    MeasurementsPerRoadSegmentSerializer,
    RoadSegmentWriteSerializer,
    StatusResponseSerializer,
)
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from api.filters.road_segment_filters import RoadSegmentFilter
from api.business.speed_interval_business import SpeedIntervalBusiness


@extend_schema_view(
    list=extend_schema(
        description="Lista todos os segmentos de estrada",
        responses=RoadSegmentSerializer(many=True),
        parameters=[
            OpenApiParameter(
                name="traffic_intensity",
                description=(
                    "Filtra por intensidade de tráfego da última medição. \n \n"
                    "Valores possíveis (velocidades em km/h): \n"
                    f"{SpeedIntervalBusiness.get_current_intervals()}"
                ),
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retorna um segmento de estrada específico",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID interno do segmento de estrada",
                required=True,
            ),
        ],
        responses=RoadSegmentSerializer,
    ),
    create=extend_schema(
        description="Cria um novo segmento de estrada",
        request=RoadSegmentWriteSerializer,
        responses=StatusResponseSerializer,
    ),
    update=extend_schema(
        description="Atualiza um segmento de estrada existente",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID interno do segmento de estrada",
                required=True,
            ),
        ],
        request=RoadSegmentWriteSerializer,
        responses=StatusResponseSerializer,
    ),
    destroy=extend_schema(
        description="Exclui um segmento de estrada",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID interno do segmento de estrada",
                required=True,
            ),
        ],
        responses=StatusResponseSerializer,
    ),
)
class RoadSegmentViewSet(ViewSet):
    """
    Viewset para retorno de dados partindo de segmentos de estrada.
    """

    # Preciso disso porque o drf_spectacular está enxergando
    # "id" como parâmetro por alguma razão, não entendo o pq
    lookup_field = "id"
    lookup_url_kwarg = "id"
    lookup_value_regex = r"\d+"

    http_method_names = ["post", "get", "put", "delete"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request):
        data = RoadSegmentRepository.get_all_road_segments()

        # traffic_intensity
        filterset = RoadSegmentFilter(request.GET, queryset=data)

        filtered_data = filterset.qs

        return Response(
            RoadSegmentSerializer(filtered_data, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, id):
        data = RoadSegmentRepository.get_road_segment_by_id(id=id)
        return Response(RoadSegmentSerializer(data).data, status=status.HTTP_200_OK)

    def destroy(self, request, id=None):
        response = RoadSegmentRepository.delete_road_segment_by_id(id=id)
        return Response({"status": response}, status=status.HTTP_200_OK)

    def update(self, request, id):
        response = RoadSegmentRepository.update_road_segment(
            id=id, new_data=request.data
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

    @extend_schema(
        description="Retorna a quantidade de medições de velocidade por segmento de estrada",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID interno do segmento de estrada",
                required=True,
            ),
        ],
        responses=MeasurementsPerRoadSegmentSerializer(many=True),
    )
    def get(self, request):
        response = RoadSegmentRepository.get_speed_measurements_per_road()
        return Response(
            MeasurementsPerRoadSegmentSerializer(response, many=True).data,
            status=status.HTTP_200_OK,
        )
