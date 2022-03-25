import pytest
from mixer.backend.django import mixer

from repositorium.learning_resources.exceptions import (
    CategoryAlreadyExists,
    CategoryDoesNotExists,
)
from repositorium.learning_resources.managers import category as category_manager


@pytest.fixture
def data_structure_category():
    yield mixer.blend("learning_resources.Category", name="Data Structures")


@pytest.mark.django_db
def test_category_exists(data_structure_category):
    assert category_manager.category_exists(name=data_structure_category.name)


@pytest.mark.django_db
def test_category_not_exists():
    name = "Cosme Fulanito"
    assert not category_manager.category_exists(name=name)


@pytest.mark.django_db
def test_create_existant_category(data_structure_category):
    with pytest.raises(CategoryAlreadyExists):
        category_manager.create_category(name=data_structure_category.name)


@pytest.mark.django_db
def test_create_category():
    name = "Cosme Fulanito"
    category = category_manager.create_category(name=name)
    assert category.name == name


@pytest.mark.parametrize(
    "function, parameter",
    [
        (category_manager.get_category_by_name, "Cosme Fulanito"),
        (category_manager.get_category_by_uuid, "e4cacd98-8811-4f88-afef-37e72718ba83"),
    ],
)
@pytest.mark.django_db
def test_get_non_existant_category(function, parameter):
    with pytest.raises(CategoryDoesNotExists):
        function(parameter)


@pytest.mark.parametrize(
    "function, attribute",
    [
        (category_manager.get_category_by_name, "name"),
        (category_manager.get_category_by_uuid, "uuid"),
    ],
)
@pytest.mark.django_db
def test_get_category(data_structure_category, function, attribute):
    category = function(getattr(data_structure_category, attribute))
    assert category == data_structure_category


@pytest.mark.django_db
def test_get_or_create_category(data_structure_category):
    created_category, created_boolean = category_manager.get_or_create_category(
        name=data_structure_category.name
    )
    assert not created_boolean
    assert created_category == data_structure_category
    _, non_created_boolean = category_manager.get_or_create_category(
        name="Non existant name"
    )
    assert non_created_boolean
