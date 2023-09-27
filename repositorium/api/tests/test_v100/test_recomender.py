import pytest

pytestmark = pytest.mark.django_db


from mixer.backend.django import mixer

from repositorium.recomendations.recomendation_models import (
    manager as recomendation_model_manager,
)


@pytest.fixture
def recomender_basename():
    yield "recomender"


def test_get_all_recomendation_models(
    get_auth_client, get_list_url, user, recomender_basename
):
    amount_recomendation_model = len(recomendation_model_manager.RECOMENDATION_MODELS)
    url = get_list_url(recomender_basename)
    client = get_auth_client(user)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data["recomendation_models"]) == amount_recomendation_model


def test_get_latest_created_model(
    get_auth_client, get_extra_url, user, learning_object, recomender_basename
):
    other_user = mixer.blend("users.User")
    expected_learning_object = mixer.blend(
        "learning_resources.LearningObject", creator_email=other_user.email
    )
    basic_uuid = recomendation_model_manager.LAST_CREATED_MODEL.uuid
    uuid = user.uuid
    url = get_extra_url(recomender_basename, "get_recomendation", {"pk": basic_uuid})
    client = get_auth_client(user)
    data = {"uuid": uuid}
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data["uuid"] == str(expected_learning_object.uuid)
