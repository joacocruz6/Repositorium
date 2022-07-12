import pytest
from freezegun import freeze_time
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


@pytest.fixture
def algorithm_category_name():
    yield "Algorithm"


@pytest.fixture
def category_basename():
    yield "category"


@freeze_time("1997-05-05")
def test_create_category(
    user, get_auth_client, get_create_url, category_basename, algorithm_category_name
):
    url = get_create_url(category_basename)
    data = {"name": algorithm_category_name}
    client = get_auth_client(user)
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 201
    assert response.data["name"] == algorithm_category_name
    assert response.data["created_at"] == "1997-05-05T00:00:00Z"


@freeze_time("1997-05-05")
@pytest.mark.parametrize(
    "already_created_category_name, category_name",
    [("Algorithm", "Algorithm"), ("Algorithm", "algorithm")],
)
def test_create_existant_category(
    user,
    get_auth_client,
    get_create_url,
    category_basename,
    already_created_category_name,
    category_name,
):
    mixer.blend("learning_resources.Category", name=already_created_category_name)
    url = get_create_url(category_basename)
    data = {"name": category_name}
    client = get_auth_client(user)
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 400
    assert response.data["errors"]["name"] == [
        "Category with that name already exists."
    ]


@freeze_time("1997-05-05")
def test_get_all_categories(user, get_auth_client, get_list_url, category_basename):
    mixer.cycle(5).blend("learning_resources.Category")
    url = get_list_url(category_basename)
    client = get_auth_client(user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["page_number"] == 1
    assert not response.data["has_next_page"]
    assert len(response.data["categories"]) == 5


def test_retrieve_category(user, get_auth_client, get_method_url, category_basename):
    category = mixer.blend("learning_resources.Category")
    url = get_method_url(category_basename, str(category.uuid))
    client = get_auth_client(user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == category.name
