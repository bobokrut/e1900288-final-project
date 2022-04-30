from flask import request, redirect, Blueprint, render_template, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from extensions import login_manager

from extensions import db
from .models import User

user = Blueprint("user", __name__)


@user.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user:  # checkin if user exists in the table
        flash('Email address already exists')
        return redirect(url_for('login_get'))

    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login_get'))


@user.route('/signup', methods=["GET"])
def signup_get():
    return render_template("signup.html")


@user.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True  # always remember login information

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login_get'))

    login_user(user, remember=remember)
    return redirect("/")


@user.route('/login', methods=['GET'])
def login_get():
    return render_template("login.html")


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@user.route("/", methods=["GET"])
@login_required
def index():
    return redirect(url_for("gallery.view_gallery"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
