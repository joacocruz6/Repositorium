from rest_framework import routers
from repositorium.api.v100.category import CategoryViewSet

router = routers.SimpleRouter()
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = []

urlpatterns += router.urls
