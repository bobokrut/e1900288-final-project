from io import BytesIO

from PIL import Image
from flask import Flask, request, render_template, redirect
from dotenv import load_dotenv
from os import environ
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

load_dotenv()
db.create_all()


@app.route('/images/<int:img_id>', methods=['GET'])
def get_image_from_db(img_id):
    image = GallaryImage.query.filter(GallaryImage.id == img_id).with_entities(GallaryImage.img_data).first()
    if image:
        return app.response_class(image[0], mimetype='application/octet-stream')
    return "Image not found", 404


@app.route('/thumbs/<int:img_id>', methods=['GET'])
def get_thumb_from_db(img_id):
    image = GallaryImage.query.filter(GallaryImage.id == img_id).with_entities(GallaryImage.img_thumb).first()
    if image:
        return app.response_class(image[0], mimetype='application/octet-stream')
    return "Image not found", 404


@app.route("/", methods=["GET"])
def index():
    images = GallaryImage.query.with_entities(GallaryImage.id, GallaryImage.img_width, GallaryImage.img_height).all()
    return render_template("index.html", images=images)


@app.route('/upload', methods=["POST"])
def upload():  # put application's code here
    filename = request.files.get("photo").filename
    ext = filename.split(".")[1]
    ext = ext if ext != "jpg" else "jpeg"
    blob = request.files.get("photo").read()

    image = Image.open(request.files.get("photo"))
    height = image.height
    width = image.width
    image.thumbnail(size=(250, 250))
    stream = BytesIO()
    image.save(stream, ext)

    image = GallaryImage(img_filename=filename, img_data=blob, img_thumb=stream.getvalue(), img_width=width, img_height=height)
    db.session.add(image)
    db.session.commit()

    return redirect("/")
