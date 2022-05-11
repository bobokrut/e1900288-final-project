from extensions import db
import env_var
import os

env_var.IMAGES_FOLDER = os.path.join(os.path.dirname(__file__), "gallery", "images")
env_var.THUMBS_FOLDER = os.path.join(os.path.dirname(__file__), "gallery", "thumbs")

pytest_plugins = [
    "tests.fixtures",
]


def pytest_configure() -> None:

    from .fixtures import app

    app.config.update({"TESTING": True})

    with app.app_context():
        db.create_all()
