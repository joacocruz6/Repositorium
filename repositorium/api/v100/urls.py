from rest_framework import routers

from repositorium.api.v100.category import CategoryViewSet
from repositorium.api.v100.learning_objects import LearningObjectViewSet
from repositorium.api.v100.systems import SystemViewSet
from repositorium.api.v100.users import AuthViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"user", UserViewSet, basename="user")
router.register(r"system", SystemViewSet, basename="system")
router.register(r"learning_object", LearningObjectViewSet, basename="learning_object")
router.register(r"auth", AuthViewSet, basename="authentication")

urlpatterns = []

urlpatterns += router.urls
