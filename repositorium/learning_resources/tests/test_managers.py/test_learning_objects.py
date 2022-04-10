import arrow
import pytest
from freezegun import freeze_time
from mixer.backend.django import mixer

from repositorium.learning_resources.exceptions import (
    LearningObjectAlreadyExists,
    LearningObjectDoesNotExists,
)
from repositorium.learning_resources.managers import (
    learning_objects as learning_objects_manager,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    email = "cosme@fulanito.com"
    yield mixer.blend("users.User", email=email)


@pytest.fixture
def system():
    yield mixer.blend("learning_resources.System")


@pytest.fixture
def categories():
    yield list(mixer.cycle(count=6).blend("learning_resources.Category"))


@pytest.fixture
def learning_object(user, system, categories):
    name = "Acelerador de protones"
    content = "Profesor cerebron, yo he trabajado mas de 50 años en una planta nuclear y creo que se como funciona un acelerador de protones"
    learning_object = mixer.blend(
        "learning_resources.LearningObject",
        name=name,
        content=content,
        created_on=system,
        created_by=user,
    )
    learning_object.categories.add(*categories)
    yield learning_object


def test_create_learning_object(user, system, categories):
    extra_data = {"a": 3}
    content = "This is the content of the learning object"
    title = "Test object"
    learning_object = learning_objects_manager.create_learning_object(
        title=title,
        content=content,
        categories=categories,
        created_on=system,
        created_by=user,
        extra_data=extra_data,
    )
    assert learning_object.created_on == system
    assert learning_object.created_by == user
    assert learning_object.categories.count() == len(categories)


def test_already_name_taken_learning_object(user, system, categories):
    title = "Test"
    mixer.blend("learning_resources.LearningObject", title=title)
    content = "Some content"
    with pytest.raises(LearningObjectAlreadyExists):
        learning_objects_manager.create_learning_object(
            title=title,
            content=content,
            categories=categories,
            created_on=system,
            created_by=user,
        )


@pytest.mark.parametrize(
    "attr_name, function",
    [
        ("uuid", learning_objects_manager.get_learning_object_by_uuid),
        ("title", learning_objects_manager.get_learning_object_by_title),
    ],
)
def test_get_learning_object(attr_name, function, learning_object):
    attr = getattr(learning_object, attr_name)
    obj = function(attr)
    assert learning_object == obj


@pytest.mark.parametrize(
    "attr_name, function",
    [
        ("uuid", learning_objects_manager.get_learning_object_by_uuid),
        ("title", learning_objects_manager.get_learning_object_by_title),
    ],
)
def test_get_non_existant_learning_object(attr_name, function, learning_object):
    attr = getattr(learning_object, attr_name)
    learning_object.delete()
    with pytest.raises(LearningObjectDoesNotExists):
        function(attr)


@freeze_time("1997-05-05")
def test_fork_learning_object(learning_object, user):
    system = mixer.blend("learning_resources.System")
    expected_name = (
        f"Fork of {learning_object.title} by {user.full_name} at {arrow.now().datetime}"
    )
    new_learning_object = learning_objects_manager.fork_learning_object(
        learning_object, user, system
    )
    assert new_learning_object.title == expected_name
    assert new_learning_object.content == learning_object.content
    assert new_learning_object.categories.count() == learning_object.categories.count()
    assert new_learning_object.created_on == system
    assert new_learning_object.created_on != learning_object.created_on
    assert new_learning_object.extra_data == learning_object.extra_data
