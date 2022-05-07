from os import path
from flask import (
    request,
    redirect,
    abort,
    Blueprint,
    render_template,
    Response,
    send_from_directory,
)
from flask.helpers import url_for
from flask_login import login_required, current_user

from env_var import IMAGES_FOLDER, THUMBS_FOLDER
from .models import GalleryImage
from PIL import Image
from extensions import db
import uuid
from psycopg2.errors import UniqueViolation
from traceback import print_exception

gallery = Blueprint("gallery", __name__)


@gallery.route("/images/<int:img_id>", methods=["GET"])
@login_required
def get_image_from_db(img_id):
    image = (
        GalleryImage.query.filter(
            GalleryImage.id == img_id, GalleryImage.user_id == current_user.id
        )
        .with_entities(GalleryImage.img_path)
        .first()
    )
    if image:
        return send_from_directory(IMAGES_FOLDER, image[0])
    abort(404)


@gallery.route("/images/<int:img_id>", methods=["POST"])
@login_required
def delete_image_from_db(img_id):

    GalleryImage.query.filter(
        GalleryImage.id == img_id, GalleryImage.user_id == current_user.id
    ).delete()
    db.session.commit()
    return redirect(url_for("gallery.view_gallery"))


@gallery.route("/thumbs/<int:img_id>", methods=["GET"])
@login_required
def get_thumb_from_db(img_id):

    image = (
        GalleryImage.query.filter(
            GalleryImage.id == img_id, GalleryImage.user_id == current_user.id
        )
        .with_entities(GalleryImage.thumb_path)
        .first()
    )
    if image:
            return send_from_directory(THUMBS_FOLDER, image[0])
    abort(404)


@gallery.route("/upload", methods=["POST"])
@login_required
def upload():
    def create_uuid(ext: str) -> tuple[str, str]:
        return f"{str(uuid.uuid4())}.{ext}", f"{str(uuid.uuid4())}.{ext}"

    for file in request.files.getlist("photo"):

        filename = file.filename
        ext = filename.split(".")[1]
        ext = ext if ext != "jpg" else "jpeg"
        image = Image.open(file)
        height = image.height
        width = image.width
        image.thumbnail(size=(250, 250))

        while True:
            image_path, thumb_path = create_uuid(ext)
            image_to_save = GalleryImage(
                img_name=filename,
                img_path=image_path,
                thumb_path=thumb_path,
                img_width=width,
                img_height=height,
                user_id=current_user.id,
            )
            try:
                db.session.add(image_to_save)
                db.session.commit()
                break
            except UniqueViolation:
                pass
        image.save(path.join(THUMBS_FOLDER, thumb_path))
        file.seek(0)
        file.save(path.join(IMAGES_FOLDER, image_path))

    return redirect("/")


@gallery.route("/")
@login_required
def view_gallery():
    images = GalleryImage.query.filter(GalleryImage.user_id == current_user.id).all()
    return render_template("index.html", images=images, username=current_user.username)
