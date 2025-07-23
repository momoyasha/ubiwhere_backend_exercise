# filters.py
import django_filters
from django.db.models import OuterRef, Subquery
from api.models.road_segment import RoadSegment
from api.models.speed_measurement import SpeedMeasurement

import logging

logger = logging.getLogger(__name__)


class RoadSegmentFilter(django_filters.FilterSet):
    # declara o filtro
    traffic_intensity = django_filters.CharFilter(
        method="filter_by_last_traffic_intensity"
    )

    def filter_by_last_traffic_intensity(self, queryset, name, value):
        # cria um queryset de SpeedMeasurements ordenados + outerref para ligação

        latest_measurements = SpeedMeasurement.objects.filter(
            road_segment=OuterRef("pk")
        ).order_by("-created_at")

        # resolve o outerref, pega apenas o SpeedMeasurement mais recente
        # para cada road_segment (o queryset original)
        annotated = queryset.annotate(
            last_speed_measurement_id=Subquery(latest_measurements.values("id")[:1]),
        )

        # carrega em lote os objetos SpeedMeasurement anotados
        measurement_ids = [
            seg.last_speed_measurement_id
            for seg in annotated
            if seg.last_speed_measurement_id
        ]
        measurement_map = SpeedMeasurement.objects.in_bulk(measurement_ids)

        # filtra em Python usando a propriedade traffic_intensity
        valid_segment_ids = []
        for seg in annotated:
            measurement = measurement_map.get(seg.last_speed_measurement_id)

            # if seg.id == 15:
            # logger.info(seg)
            # logger.info(seg.last_speed_measurement_id)
            # logger.info(measurement)

            if not measurement:
                continue

            # traffic_intensity é um dict com 'criticality_text'
            text = measurement.traffic_intensity["criticality_text"]

            # logger.info(measurement.traffic_intensity)
            # logger.info(measurement.traffic_intensity["criticality_text"])
            if text and text.lower() == value.lower():
                valid_segment_ids.append(seg.id)

        # 4️⃣ Retorna só os RoadSegments cujos IDs passaram no teste
        return queryset.filter(id__in=valid_segment_ids)

    class Meta:
        model = RoadSegment
        fields = []
