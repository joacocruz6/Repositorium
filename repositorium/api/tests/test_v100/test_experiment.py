import uuid

import pytest

pytestmark = pytest.mark.django_db

from mixer.backend.django import mixer


@pytest.fixture
def experiment_basename():
    yield "experiment"


def test_create_experiment(get_auth_client, user, get_create_url, experiment_basename):
    url = get_create_url(experiment_basename)
    client = get_auth_client(user)
    response = client.post(url, content_type="application/json")
    assert response.status_code == 201
    assert response.data is not None


def test_finish_experiment(get_auth_client, user, get_put_url, experiment_basename):
    client = get_auth_client(user)
    experiment = mixer.blend("recomendations.Experiment", user=user)
    url = get_put_url(experiment_basename, str(experiment.uuid))
    chosen_recomendation = str(uuid.uuid4())
    model_chosen = str(uuid.uuid4())
    data = {
        "model": model_chosen,
        "item": chosen_recomendation,
    }
    response = client.put(url, data=data, content_type="application/json")
    assert response.status_code == 200


def test_try_finish_other_experiment(
    get_auth_client, user, get_put_url, experiment_basename
):
    client = get_auth_client(user)
    other_user = mixer.blend("users.User")
    experiment = mixer.blend("recomendations.Experiment", user=other_user)
    chosen_recomendation = str(uuid.uuid4())
    model_chosen = str(uuid.uuid4())
    data = {
        "model": model_chosen,
        "item": chosen_recomendation,
    }
    url = get_put_url(experiment_basename, experiment.uuid)
    response = client.put(url, data=data, content_type="application/json")
    assert response.status_code == 404
