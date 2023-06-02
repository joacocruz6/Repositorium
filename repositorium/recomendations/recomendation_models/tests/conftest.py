import pytest
from mixer.backend.django import mixer


@pytest.fixture
def user_email():
    yield "cosme@fulanito.com"


@pytest.fixture
def user(user_email):
    yield mixer.blend("users.User", email=user_email)


@pytest.fixture
def categories():
    yield list(mixer.cycle(count=6).blend("learning_resources.Category"))


@pytest.fixture
def system():
    yield mixer.blend("learning_resources.System", name="Nintendo 64!!!")


@pytest.fixture
def learning_object_factory():
    def _learning_object_factory(lo_categories, creator=None, system_created=None):
        learning_object_kwargs = dict()
        if creator is not None:
            learning_object_kwargs["creator_email"] = creator.email
        if system_created is not None:
            learning_object_kwargs["created_on"] = system_created
        learning_object = mixer.blend(
            "learning_resources.LearningObject", **learning_object_kwargs
        )
        learning_object.categories.add(*lo_categories)
        return learning_object

    yield _learning_object_factory
