import pytest
from mixer.backend.django import mixer

from repositorium.recomendations.recomendation_models import (
    basic_filter as recomendation_model,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def model():
    yield recomendation_model.ProfileLastFilteredModel()


def test_basic_filter(model, user, learning_object_factory, categories, system):
    first_lo = learning_object_factory(categories[:3])
    second_lo = learning_object_factory(categories[2:])
    third_lo = learning_object_factory([categories[4]])
    fourth_lo = learning_object_factory([categories[3], categories[4]])
    mixer.blend(
        "learning_resources.LearningObjectUsage",
        user=user,
        learning_object=second_lo,
        used_on=system,
    )
    recomendation = model.get_recomendation(user.email)
    assert recomendation == fourth_lo
