import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_healthz(client):
    url = reverse("api:health")
    response = client.get(url)
    assert response.status_code == 200
