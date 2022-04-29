from io import BytesIO

from PIL import Image
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
DATABASE_URL = environ.get("DATABASE_URL")  # in Heroku this variable is always presenting
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL.replace(DATABASE_URL.split("://")[0], "postgresql+psycopg2", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")  # is needed for login to work
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login_get'  # url for login page
login_manager.init_app(app)

from models import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup', methods=['POST'])
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


@app.route('/signup', methods=["GET"])
def signup_get():
    return render_template("signup.html")


@app.route('/login', methods=['POST'])
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


@app.route('/login', methods=['GET'])
def login_get():
    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/images/<int:img_id>', methods=['GET'])
@login_required
def get_image_from_db(img_id):
    image = GalleryImage.query.filter(GalleryImage.id == img_id, GalleryImage.user_id == current_user.id).with_entities(GalleryImage.img_data).first()
    if image:
        return app.response_class(image[0], mimetype='application/octet-stream')
    return "Image not found", 404


@app.route('/thumbs/<int:img_id>', methods=['GET'])
@login_required
def get_thumb_from_db(img_id):
    image = GalleryImage.query.filter(GalleryImage.id == img_id, GalleryImage.user_id == current_user.id).with_entities(GalleryImage.img_thumb).first()
    if image:
        return app.response_class(image[0], mimetype='application/octet-stream')
    return "Image not found", 404


@app.route("/", methods=["GET"])
@login_required
def index():
    images = GalleryImage.query.filter(GalleryImage.user_id == current_user.id).with_entities(GalleryImage.id, GalleryImage.img_width, GalleryImage.img_height).all()
    return render_template("index.html", images=images, username=current_user.username)


@app.route('/upload', methods=["POST"])
@login_required
def upload():
    filename = request.files.get("photo").filename
    ext = filename.split(".")[1]
    ext = ext if ext != "jpg" else "jpeg"
    blob = request.files.get("photo").read()

    # start of the thumbnail creation
    image = Image.open(request.files.get("photo"))
    height = image.height
    width = image.width
    image.thumbnail(size=(250, 250))
    stream = BytesIO()
    image.save(stream, ext)
    # end
    image = GalleryImage(img_filename=filename, img_data=blob, img_thumb=stream.getvalue(), img_width=width, img_height=height, user_id=current_user.id)
    db.session.add(image)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    db.create_all()  # creating tables in the database
    app.run(debug=False)
