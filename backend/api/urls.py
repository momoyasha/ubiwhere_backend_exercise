from rest_framework.routers import DefaultRouter
from api.views.speed_measurement_views import SpeedMeasurementViewSet

router = DefaultRouter()

router.register(
    r"speed_measurements", SpeedMeasurementViewSet, basename="speed_measurement"
)

urlpatterns = router.urls
