from io import BytesIO

from PIL import Image
from flask import Flask, request, render_template, redirect
from dotenv import load_dotenv
from os import environ
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
POSTGRES_URL = environ.get("POSTGRES_URL")
POSTGRES_USER = environ.get("POSTGRES_USER")
POSTGRES_PW = environ.get("POSTGRES_PW")
POSTGRES_DB = environ.get("POSTGRES_DB")
DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

load_dotenv()
db.create_all()

@app.route('/images/<int:img_id>', methods=['GET'])
def get_image_from_db(img_id):
    image = GallaryImage.query.get_or_404(img_id)
    return app.response_class(image.img_data, mimetype='application/octet-stream')


@app.route('/thumbs/<int:img_id>', methods=['GET'])
def get_thumb_from_db(img_id):
    image = GallaryImage.query.get_or_404(img_id)
    return app.response_class(image.img_thumb, mimetype='application/octet-stream')


@app.route("/", methods=["GET"])
def index():
    images = GallaryImage.query.all()
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

