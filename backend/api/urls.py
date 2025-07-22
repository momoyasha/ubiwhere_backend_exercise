from rest_framework.routers import DefaultRouter
from api.views.speed_measurement_views import SpeedMeasurementViewSet
from api.views.road_segment_views import RoadSegmentViewSet

router = DefaultRouter()

router.register(
    r"speed_measurements",
    SpeedMeasurementViewSet,
    basename="speed_measurement",
)
router.register(r"road_segments", RoadSegmentViewSet, basename="road_segment")


urlpatterns = router.urls
