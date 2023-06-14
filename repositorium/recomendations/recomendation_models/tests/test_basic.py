import pytest
from mixer.backend.django import mixer

from repositorium.recomendations.recomendation_models import basic
from repositorium.recomendations.recomendation_models.basic_filter import (
    ProfileLastFilteredModel,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def learning_objects():
    yield list(mixer.cycle(6).blend("learning_resources.LearningObject"))


@pytest.fixture
def basic_model():
    yield basic.SimpleLastCreatedRecomendation()


def test_get_recomendation(learning_objects, basic_model):
    recomended_lo = basic_model.get_recomendation()
    assert recomended_lo == learning_objects[-1]
