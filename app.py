from pathlib import Path

from flask import Flask, request, render_template

from extensions import db, login_manager
from env_var import *
import gallery
import user


def create_app() -> Flask:
    app = Flask(__name__)
    # app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL.replace(
    #     DATABASE_URL.rsplit("://")[0], "postgresql+psycopg2", 1
    # )
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY  # is needed for login to work
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    settings_for_ext(app)
    create_folders()
    return app


def register_extensions(app: Flask) -> None:
    """Register Flask extensions."""
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app: Flask) -> None:
    """Register Flask blueprints."""
    app.register_blueprint(user.views.user)
    app.register_blueprint(gallery.views.gallery)


def register_errorhandlers(app: Flask) -> None:
    """Register error handlers."""

    def page_not_found(error: str) -> tuple[str, int]:
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        if request.path.startswith("/images/"):

            return render_template("not_found.html", what="Image", back="/"), 404
        else:

            return render_template("not_found.html", what="Page", back="/"), 404

    app.errorhandler(404)(page_not_found)


def settings_for_ext(app: Flask) -> None:
    with app.app_context():
        db.create_all()  # creating tables in the database
    login_manager.login_view = "user.login_get"  # url for login page


def create_folders() -> None:
    Path(IMAGES_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(THUMBS_FOLDER).mkdir(parents=True, exist_ok=True)
