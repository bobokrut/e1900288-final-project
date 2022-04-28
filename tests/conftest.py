from app import db, app

pytest_plugins = [
    "tests.fixtures",
]


def pytest_configure(config):
    print(f'Creating tables in {app.config.get("SQLALCHEMY_DATABASE_URI")}')
    db.create_all()

