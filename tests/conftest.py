from app import db, app
from sqlalchemy import inspect

pytest_plugins = [
    "tests.fixtures",
]


def pytest_configure(config):
    print(f'Creating tables in {app.config.get("SQLALCHEMY_DATABASE_URI")}')
    db.create_all()
    print(inspect(db.engine).get_table_names())

