from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from api.views.road_segment_views import RoadSegmentViewSet


class PermissionsTests(TestCase):
    def setUp(self):
        # para simular requisições
        self.factory = RequestFactory()
        self.user = User.objects.create_user("u", password="p")
        self.viewset = RoadSegmentViewSet()

    def test_list_retrieve_allow_any(self):
        for action in ["list", "retrieve"]:
            request = self.factory.get("/")
            request.user = AnonymousUser()
            setattr(self.viewset, "action", action)
            perms = self.viewset.get_permissions()
            self.assertTrue(any(isinstance(p, AllowAny) for p in perms))

    def test_create_requires_admin(self):
        request = self.factory.post("/")
        request.user = self.user
        setattr(self.viewset, "action", "create")
        perms = self.viewset.get_permissions()
        self.assertTrue(any(isinstance(p, IsAdminUser) for p in perms))
