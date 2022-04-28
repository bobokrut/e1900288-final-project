from app import db, app

pytest_plugins = [
    "tests.fixtures",
]


def pytest_configure(config):
    app.config.update({"TESTING": True})
    db.create_all()

