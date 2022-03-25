from rest_framework import routers

from repositorium.api.v100.category import CategoryViewSet
from repositorium.api.v100.systems import SystemViewSet
from repositorium.api.v100.users import UserViewSet

router = routers.SimpleRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"users", UserViewSet, basename="user")
router.register(r"systems", SystemViewSet, basename="system")

urlpatterns = []

urlpatterns += router.urls
