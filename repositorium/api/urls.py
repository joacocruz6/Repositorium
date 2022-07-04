from django.urls import include, path

from repositorium.api.views import healthz

app_name = "api"
urlpatterns = [
    path("healthz/", healthz, name="health"),
    path("v100/", include("repositorium.api.v100.urls")),
]
