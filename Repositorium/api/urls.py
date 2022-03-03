from django.urls import path
from repositorium.api.views import healthz

app_name = "api"
urlpatterns = [path("healtz/", healthz, name="health")]
