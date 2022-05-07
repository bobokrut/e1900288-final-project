from flask_login import current_user
from flask import get_flashed_messages


def test_gallery_without_login(anonymous_client):
    with anonymous_client:
        response = anonymous_client.get("/", follow_redirects=True)
        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/login"


def test_image_without_login(anonymous_client):
    with anonymous_client:
        response = anonymous_client.get("/images/1", follow_redirects=True)

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/login"


def test_image_with_login(client):
    response = client.get("/images/1")

    assert response.status_code == 200 or b"Image not found" in response.data
    assert len(response.history) == 0
    assert response.request.path == "/images/1"
    assert current_user.username == "test"


def test_gallery_with_login(client):
    response = client.get("/")

    assert response.status_code == 200
    assert len(response.history) == 0
    assert response.request.path == "/"
    assert current_user.username == "test"


def test_cant_signup_two_times(client_for_signin):
    response = client_for_signin.post(
        "/signup",
        data={"email": "test@test.com", "username": "test", "password": "test"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/login"
    assert len(get_flashed_messages()) == 1
    assert "Username already exists" in get_flashed_messages()


def test_wrong_password(client_for_signin):
    response = client_for_signin.post(
        "/login", data={"username": "test", "password": "test1"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/login"
    assert len(get_flashed_messages()) == 1
    assert "Please check your login details and try again." in get_flashed_messages()


def test_wrong_username(client_for_signin):
    response = client_for_signin.post(
        "/login", data={"username": "test1", "password": "test"}, follow_redirects=True
    )
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/login"
    assert len(get_flashed_messages()) == 1
    assert "Please check your login details and try again." in get_flashed_messages()
