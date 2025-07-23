from rest_framework.response import Response
from rest_framework import status
from api.serializers.sensor_data_serializer import (
    SensorDataSerializer,
    SensorDataByCarSerializer,
)
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from api.business.sensor_business import SensorBusiness


# para criar a permissão customizada
from rest_framework.permissions import BasePermission
from django.conf import settings


class SensorAPIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-Key") or request.query_params.get(
            "api_key"
        )
        return api_key == settings.SENSOR_API_KEY


@extend_schema_view(
    create=extend_schema(
        description="Recebe dados de sensores e grava na base de dados",
        request=SensorDataSerializer(many=True),
        responses={201: None, 400: None},
    )
)
class SensorDataViewSet(ViewSet):
    """
    Viewset para gravação de dados de sensores.
    """

    http_method_names = ["post"]

    permission_classes = [SensorAPIKeyPermission]

    def create(self, request):
        serializer = SensorDataSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        description="Retorna dados referentes a um carro a partir da placa.",
        request=SensorDataSerializer(many=True),
        responses={201: None, 400: None},
        parameters=[
            OpenApiParameter(
                name="license_plate",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Código da placa do carro",
                required=True,
            ),
        ],
    )
)
class SensorDataByCarView(APIView):
    """
    Retorna dados referentes a um carro a partir da placa.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        license_plate = request.query_params.get("license_plate")

        if not license_plate:
            return Response(
                {"error": "Parâmetro 'license_plate' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = SensorBusiness.get_data_by_car(license_plate=license_plate)
        return Response(
            SensorDataByCarSerializer(response).data,
            status=status.HTTP_200_OK,
        )
