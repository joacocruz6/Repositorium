import pytest
from mixer.backend.django import mixer

from repositorium.learning_resources.exceptions import (
    SystemAlreadyExists,
    SystemDoesNotExists,
)
from repositorium.learning_resources.managers import system as system_manager


@pytest.fixture
def non_existant_system_name():
    yield "Cosme Fulanito"


@pytest.fixture
def easyexam_system():
    yield mixer.blend("learning_resources.System", name="EasyExam")


@pytest.mark.django_db
def test_non_existant_system(non_existant_system_name):
    assert not system_manager.system_exists(name=non_existant_system_name)


@pytest.mark.django_db
def test_system_exists(easyexam_system):
    assert system_manager.system_exists(name=easyexam_system.name)


@pytest.mark.django_db
def test_create_system(non_existant_system_name):
    system = system_manager.create_system(name=non_existant_system_name)
    assert system.name == non_existant_system_name


@pytest.mark.django_db
def test_create_existant_system(easyexam_system):
    with pytest.raises(SystemAlreadyExists):
        system_manager.create_system(name=easyexam_system.name)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "function, parameter",
    [
        (system_manager.get_system_by_name, "Cosme Fulanito"),
        (system_manager.get_system_by_uuid, "aa202582-6c8c-4469-8850-e360a6a38e95"),
    ],
)
def test_get_non_existant_system(function, parameter):
    with pytest.raises(SystemDoesNotExists):
        function(parameter)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "function, attribute_name",
    [
        (system_manager.get_system_by_name, "name"),
        (system_manager.get_system_by_uuid, "uuid"),
    ],
)
def test_get_system(function, attribute_name, easyexam_system):
    system = function(getattr(easyexam_system, attribute_name))
    assert system == easyexam_system
