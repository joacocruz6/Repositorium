import pytest
from django.urls import reverse
from mixer.backend.django import mixer


@pytest.fixture
def get_create_url():
    def _create_url(basename: str):
        return reverse(f"api:{basename}-list")

    yield _create_url


@pytest.fixture
def get_list_url():
    def _list_url(basename: str):
        return reverse(f"api:{basename}-list")

    yield _list_url


@pytest.fixture
def get_put_url():
    def _put_url(basename: str, pk: str):
        return reverse(f"api:{basename}-detail", kwargs={"pk": pk})

    yield _put_url


@pytest.fixture
def get_method_url():
    def _get_url(basename: str, pk: str):
        return reverse(f"api:{basename}-detail", kwargs={"pk": pk})

    yield _get_url


@pytest.fixture
def get_delete_url():
    def _delete_url(basename: str, pk: str):
        return reverse(f"api:{basename}-detail", kwargs={"pk": pk})

    yield _delete_url


@pytest.fixture
def get_extra_url():
    def _extra_url(basename: str, url_name: str, kwargs=None):
        return reverse(f"api:{basename}-{url_name}", kwargs=kwargs)

    yield _extra_url


@pytest.fixture
def user_email():
    yield "cosme@fulanito.com"


@pytest.fixture
def user(user_email):
    yield mixer.blend(
        "users.User", email=user_email, first_name="Cosme", last_name="Fulanito"
    )


@pytest.fixture
def category():
    yield mixer.blend("learning_resources.Category", name="Hey it's me")


@pytest.fixture
def system():
    yield mixer.blend("learning_resources.System", name="Nintendo 64!!!")


@pytest.fixture
def learning_object(user, category, system):
    learning_object = mixer.blend(
        "learning_resources.LearningObject",
        title="Testing in Java",
        created_on=system,
        created_by=user,
    )
    learning_object.categories.add(category)
    yield learning_object
