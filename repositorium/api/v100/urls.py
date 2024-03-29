from django.urls import path
from rest_framework import routers

from repositorium.api.v100.category import CategoryViewSet
from repositorium.api.v100.experiments import ExperimentViewSet
from repositorium.api.v100.learning_objects import LearningObjectViewSet
from repositorium.api.v100.learning_objects_files import FileManagementAPIView
from repositorium.api.v100.recomender import RecomenderViewSet
from repositorium.api.v100.systems import SystemViewSet
from repositorium.api.v100.users import AuthViewSet, UserViewSet

router = routers.SimpleRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"user", UserViewSet, basename="user")
router.register(r"system", SystemViewSet, basename="system")
router.register(r"learning_object", LearningObjectViewSet, basename="learning_object")
router.register(r"auth", AuthViewSet, basename="authentication")
router.register(r"recomend", RecomenderViewSet, basename="recomender")
router.register(r"experiment", ExperimentViewSet, basename="experiment")

urlpatterns = [
    path(
        "learning_object/files/<uuid:uuid>/",
        FileManagementAPIView.as_view(),
        name="file_management_view",
    ),
]

urlpatterns += router.urls
