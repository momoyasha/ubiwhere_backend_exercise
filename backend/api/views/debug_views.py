from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from api.business.speed_measurement_business import SpeedMeasurementBusiness
from api.business.speed_interval_business import SpeedIntervalBusiness
from api.business.sensor_business import SensorBusiness


class DebugView(APIView):
    """
    View para chamar lógica em desenvolvimento.
    Útil para debugging.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        method_to_debug = "a"
        return Response({"status": True}, status=status.HTTP_200_OK)


class PopulateInitialDataView(APIView):
    """
    Popula a base de dados com os dados iniciais fornecidos em traffic_speed.csv.
    Também cria intervalos de velocidade para referência.
    """

    def get(self, request):
        SpeedMeasurementBusiness.populate_database_with_initial_data()
        SpeedIntervalBusiness.populate_database_with_initial_data()
        SensorBusiness.populate_database_with_initial_data()
        return Response({"status": True}, status=status.HTTP_200_OK)
