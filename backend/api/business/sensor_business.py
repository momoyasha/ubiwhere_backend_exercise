from api.models.sensor import Sensor
from api.models.car import Car
from api.models.sensor_data import SensorData
import csv
from django.conf import settings
from django.utils.timezone import now, timedelta


import logging

logger = logging.getLogger(__name__)


class SensorBusiness:
    """
    Classe de métodos para tratar objetos relacionados a Sensor.
    """

    def populate_database_with_initial_data():
        """
        Carga inicial na base de dados a partir do csv fornecido no exercício.
        """
        sensor_list = []

        file_path = settings.BASE_DIR / "data" / "sensors.csv"

        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                sensor = Sensor(sensor_id=row["id"], name=row["name"], uuid=row["uuid"])
                sensor_list.append(sensor)
            try:
                Sensor.objects.bulk_create(sensor_list)
            except Exception as ex:
                logger.info(ex)

    @staticmethod
    def get_data_by_car(license_plate: str):
        """
        Retorna dados do carro e passagens registradas
        nas últimas 24 horas.
        """
        try:
            car_obj = Car.objects.get(license_plate=license_plate)
        except Car.DoesNotExist:
            return None

        # medições das últimas 24 horas
        datetime_since = now() - timedelta(hours=24)

        sensor_data = SensorData.objects.filter(
            car=car_obj, timestamp__gte=datetime_since
        )

        response = {"car": car_obj, "sensor_data": sensor_data}

        return response
