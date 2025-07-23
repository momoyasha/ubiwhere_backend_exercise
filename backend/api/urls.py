from rest_framework.routers import DefaultRouter
from api.views.speed_measurement_views import SpeedMeasurementViewSet
from api.views.road_segment_views import RoadSegmentViewSet, RoadSegmentRelatedDataView
from django.urls import path
from api.views.sensor_data_views import SensorDataViewSet

router = DefaultRouter()

router.register(
    r"speed_measurements",
    SpeedMeasurementViewSet,
    basename="speed_measurement",
)

router.register(r"road_segments", RoadSegmentViewSet, basename="road_segment")
router.register(r"sensor_data", SensorDataViewSet, basename="sensor_data")


api_view_patterns = [
    path(
        "measurements_per_road/",
        RoadSegmentRelatedDataView.as_view(),
        name="measurements-per-road",
    ),
]

urlpatterns = router.urls + api_view_patterns
