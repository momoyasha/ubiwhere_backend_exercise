from api.models.speed_measurement import SpeedMeasurement
import csv
from django.conf import settings
from django.contrib.gis.geos import Point


class SpeedMeasurementBusiness:
    """
    Classe de métodos para tratar objetos SpeedMeasurement.
    """

    def populate_database_with_initial_data():
        """
        Carga inicial na base de dados a partir do csv fornecido no exercício.
        """
        data_points = []

        file_path = settings.BASE_DIR / "data" / "traffic_speed.csv"

        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                obj = SpeedMeasurement(
                    measurement_id=row["ID"],
                    start_point=Point(
                        float(row["Long_start"]), float(row["Lat_start"])
                    ),
                    end_point=Point(float(row["Long_end"]), float(row["Lat_end"])),
                    length=row["Length"],
                    speed=float(row["Speed"]),
                )

                data_points.append(obj)

            SpeedMeasurement.objects.bulk_create(data_points)
