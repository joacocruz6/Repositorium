import uuid

import pytest

pytestmark = pytest.mark.django_db

from mixer.backend.django import mixer


@pytest.fixture
def learning_object_basename():
    yield "learning_object"


def test_create_learning_object_view(
    get_auth_client, user, category, system, get_create_url, learning_object_basename
):
    url = get_create_url(learning_object_basename)
    data = {
        "title": "Design Patterns in Shrek",
        "content": "Somebody once told me, the world is gonna roll me.",
        "categories": [category.name],
        "system_uuid": str(system.uuid),
        "description": "Song of Shrek",
        "extra_data": {
            "renders": "latex",
        },
    }
    client = get_auth_client(user)
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 201
    assert response.data["title"] == "design patterns in shrek"
    assert (
        response.data["content"] == "Somebody once told me, the world is gonna roll me."
    )
    assert len(response.data["categories"]) == 1
    assert response.data["categories"][0]["uuid"] == str(category.uuid)
    assert response.data["categories"][0]["name"] == category.name
    assert len(response.data["extra_data"]) == 1
    assert response.data["extra_data"]["renders"] == "latex"
    assert not response.data["is_forked"]
    assert response.data["creator_email"] == user.email
    assert response.data["system"] == system.name


def test_not_existant_system_create_learning_object(
    get_auth_client, user, category, get_create_url, learning_object_basename
):
    url = get_create_url(learning_object_basename)
    client = get_auth_client(user)
    data = {
        "title": "Shrek",
        "content": "Shrek is love, Shrek is life.",
        "description": "Video of shrek",
        "categories": [category.name],
        "system_uuid": str(uuid.uuid4()),
        "extra_data": {},
    }
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 404


def test_non_existant_category_create_learning_object(
    get_auth_client, user, system, get_create_url, learning_object_basename
):
    url = get_create_url(learning_object_basename)
    client = get_auth_client(user)
    data = {
        "title": "Shrek is ...",
        "content": "Love or Life?",
        "description": "One Shrek",
        "categories": ["Hello there"],
        "system_uuid": str(system.uuid),
        "extra_data": {},
    }
    response = client.post(url, data=data, content_type="application/json")

    assert response.status_code == 201


def test_list_learning_object_view(
    get_auth_client, user, system, get_list_url, learning_object_basename
):
    mixer.cycle(5).blend(
        "learning_resources.LearningObject", created_by=user, created_on=system
    )
    url = get_list_url(learning_object_basename)
    client = get_auth_client(user)
    response = client.get(url, content_type="application/json")
    assert response.status_code == 200
    assert response.data["page_number"] == 1
    assert not response.data["has_next_page"]
    assert len(response.data["learning_objects"]) == 5


def test_filter_learning_object_view(
    get_auth_client, user, system, get_list_url, learning_object_basename
):
    learning_object = mixer.blend(
        "learning_resources.LearningObject", title="Some Title", created_on=system
    )
    categories = mixer.cycle(5).blend("learning_resources.Category")
    mixer.blend("learning_resources.LearningObject", title="Shrek").categories.set(
        categories[4:]
    )
    learning_object.categories.set(categories)
    url_category = get_list_url(learning_object_basename)
    url_title = get_list_url(learning_object_basename)
    client = get_auth_client(user)
    response_category = client.get(
        url_category,
        {"categories": ",".join([category.name for category in categories[:3]])},
        content_type="application/json",
    )
    response_title = client.get(
        url_title, {"title": "some"}, content_type="application/json"
    )
    assert response_category.status_code == 200
    assert response_title.status_code == 200
    assert response_category.data["page_number"] == 1
    assert response_title.data["page_number"] == 1
    assert not response_category.data["has_next_page"]
    assert not response_title.data["has_next_page"]
    assert len(response_category.data["learning_objects"]) == 1
    assert len(response_title.data["learning_objects"]) == 1


def test_list_learning_objects_empty(
    get_auth_client, user, get_list_url, learning_object_basename
):
    url = get_list_url(learning_object_basename)
    client = get_auth_client(user)
    response = client.get(url, content_type="application/json")
    assert response.status_code == 200
    assert response.data["page_number"] == 1
    assert not response.data["has_next_page"]
    assert len(response.data["learning_objects"]) == 0


def test_retrieve_learning_object(
    get_auth_client, user, get_method_url, learning_object_basename, learning_object
):
    url = get_method_url(learning_object_basename, str(learning_object.uuid))
    client = get_auth_client(user)
    response = client.get(url, content_type="application/json")
    assert response.status_code == 200


@pytest.fixture
def fork_url_name():
    yield "fork_learning_object"


def test_fork_learning_object(
    get_auth_client,
    user,
    learning_object,
    get_extra_url,
    learning_object_basename,
    fork_url_name,
):
    system = mixer.blend("learning_resources.System")
    kwargs = {"pk": str(learning_object.uuid)}
    data = {"system_uuid": str(system.uuid)}
    url = get_extra_url(learning_object_basename, fork_url_name, kwargs)
    client = get_auth_client(user)
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 201


def test_fork_non_existant_learning_object(
    get_auth_client, user, get_extra_url, learning_object_basename, fork_url_name
):
    system = mixer.blend("learning_resources.System")
    kwargs = {"pk": str(uuid.uuid4())}
    data = {"system_uuid": str(system.uuid)}
    url = get_extra_url(learning_object_basename, fork_url_name, kwargs)
    client = get_auth_client(user)
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 404


def test_fork_learning_object_non_existant_system(
    get_auth_client,
    user,
    get_extra_url,
    learning_object,
    learning_object_basename,
    fork_url_name,
):
    kwargs = {"pk": str(learning_object.uuid)}
    data = {"system_uuid": str(uuid.uuid4())}
    url = get_extra_url(learning_object_basename, fork_url_name, kwargs)
    client = get_auth_client(user)
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 404


def test_get_my_learning_objects(
    get_auth_client, user, get_extra_url, learning_object_basename
):
    mixer.cycle(5).blend("learning_resources.LearningObject", creator_email=user.email)
    url_name = "get_my_learning_objects"
    url = get_extra_url(learning_object_basename, url_name)
    client = get_auth_client(user)
    response = client.get(url, content_type="application/json")
    assert response.status_code == 200
