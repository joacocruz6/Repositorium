from django.urls import path
from Repositorium.api.views import healthz

urlpatterns = [path("healtz/", healthz, name="health")]
