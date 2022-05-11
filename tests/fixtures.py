from pathlib import Path
from shutil import rmtree
import os
from typing import Iterator


import pytest
from flask_login import current_user
from flask.testing import FlaskClient

from extensions import db
from app import create_app
from gallery.models import GalleryImage
from user.models import User
import env_var


app = create_app()
resources = Path(__file__).parent / "files"


@pytest.fixture()
def anonymous_client() -> FlaskClient:
    """fixture with simple client"""
    return app.test_client()


@pytest.fixture()
def client_for_signin(anonymous_client: FlaskClient) -> Iterator[FlaskClient]:
    """fixture with client that has an account"""
    with anonymous_client:
        anonymous_client.post(
            "/signup",
            data={"email": "test@test.com", "username": "test", "password": "test"},
        )
        yield anonymous_client
        User.query.filter(User.username == "test").delete()
        db.session.commit()


@pytest.fixture()
def client(anonymous_client: FlaskClient) -> Iterator[FlaskClient]:
    """fixture with logged in client"""
    with anonymous_client:
        anonymous_client.post(
            "/signup",
            data={"email": "test@test.com", "username": "test", "password": "test"},
        )
        anonymous_client.post("/login", data={"username": "test", "password": "test"})
        yield anonymous_client
        User.query.filter(User.username == "test").delete()
        db.session.commit()


@pytest.fixture()
def client_without_images(client: FlaskClient) -> Iterator[FlaskClient]:

    GalleryImage.query.filter(GalleryImage.user_id == current_user.id).delete()
    db.session.commit()

    yield client

    GalleryImage.query.filter(GalleryImage.user_id == current_user.id).delete()
    db.session.commit()

    if os.path.exists(env_var.IMAGES_FOLDER):
        rmtree(Path(env_var.IMAGES_FOLDER).parent)

    if os.path.exists(env_var.THUMBS_FOLDER):
        rmtree(Path(env_var.THUMBS_FOLDER).parent)
