import pytest
from django.urls import reverse
from repositorium.api.views import healthz


@pytest.mark.django_db
def test_healthz(client):
    url = reverse("api:health")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_healthz_view(rf):
    url = reverse("api:health")
    request = rf.get(url)
    response = healthz(request)
    assert response.status_code == 200
    assert "status" in response.data
    assert response.data["status"] == "ok"
