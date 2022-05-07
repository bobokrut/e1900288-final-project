from extensions import db

pytest_plugins = [
    "tests.fixtures",
]


from .fixtures import app


def pytest_configure(config):
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
