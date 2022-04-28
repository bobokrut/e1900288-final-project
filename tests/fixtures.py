import pytest
from app import app, db
from models import User, GalleryImage
from flask_login import current_user
from pathlib import Path

resources = Path(__file__).parent / "files"
db.create_all()

@pytest.fixture()
def anonymous_client():
    app.config.update({"TESTING": True})
    return app.test_client()


@pytest.fixture()
def client_for_signin(anonymous_client):
    with anonymous_client:
        anonymous_client.post("/signup", data={"email": "test@test.com", "username": "test", "password": "test"})
        yield anonymous_client
        User.query.filter(User.username == "test").delete()
        db.session.commit()


@pytest.fixture()
def client(anonymous_client):
    with anonymous_client:
        anonymous_client.post("/signup", data={"email": "test@test.com", "username": "test", "password": "test"})
        anonymous_client.post("/login", data={"username": "test", "password": "test"})
        yield anonymous_client
        User.query.filter(User.username == "test").delete()
        db.session.commit()


@pytest.fixture()
def client_without_images(client):
    GalleryImage.query.filter(GalleryImage.user_id == current_user.id).delete()
    db.session.commit()
    yield client
    GalleryImage.query.filter(GalleryImage.user_id == current_user.id).delete()
    db.session.commit()


@pytest.fixture()
def client_with_image(client_without_images):
    client_without_images.post("/upload", follow_redirects=True, data={
        "photo": ((resources / "pexels-pixabay-302743.jpg").open("rb"), "pexels-pixabay-302743.jpg")
    })
    yield client_without_images
