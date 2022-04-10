import pytest
from freezegun import freeze_time

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_basename():
    yield "user"


@freeze_time("1997-05-05")
def test_create_user_view(client, get_create_url, user_basename):
    url = get_create_url(user_basename)
    email = "joaquin@cruz.com"
    first_name = "Joaquin"
    last_name = "Cruz"
    password = "some_password"
    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }
    expected_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "created_at": "1997-05-05T00:00:00Z",
    }
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 201
    assert response.data == expected_data


def test_already_created_user(user, client, get_create_url, user_basename):
    url = get_create_url(user_basename)
    data = {
        "email": user.email,
        "password": "some_password",
        "first_name": "Joaquin",
        "last_name": "Cruz",
    }
    response = client.post(url, data=data, content_type="application/json")
    assert response.status_code == 400
    assert response.data is None
