from flask import request, redirect, Blueprint, render_template, url_for, flash

from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.wrappers.response import Response
from extensions import login_manager

from extensions import db
from .models import User

from typing import Any

user = Blueprint("user", __name__)


@user.route("/signup", methods=["POST"])  # type: ignore
def signup_post() -> Response:
    email: str = request.form.get("email")
    username: str = request.form.get("username")
    password: str = request.form.get("password")
    user = User.query.filter_by(username=username).first()

    if user:  # checkin if user exists in the table
        flash("Username already exists")
        return redirect(url_for("user.login_get"))

    new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))  # type: ignore

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("user.login_get"))


@user.route("/signup", methods=["GET"])  # type: ignore
def signup_get() -> str:
    return render_template("signup.html")


@user.route("/login", methods=["POST"])  # type: ignore
def login_post() -> Response:
    username: str = request.form.get("username")  # type: ignore
    password: str = request.form.get("password")  # type: ignore
    remember = True  # always remember login information

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("user.login_get"))

    login_user(user, remember=remember)
    return redirect(url_for("gallery.view_gallery"))


@user.route("/login", methods=["GET"])  # type: ignore
def login_get() -> str:
    return render_template("login.html")


@user.route("/logout")  # type: ignore
@login_required  # type: ignore
def logout() -> Response:
    logout_user()
    return redirect(url_for("user.login_get"))


@login_manager.user_loader  # type: ignore
def load_user(user_id: str) -> Any:
    return User.query.get(int(user_id))
