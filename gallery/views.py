from flask import (
    request,
    redirect,
    abort,
    Blueprint,
    render_template,
    send_from_directory,
)
from flask.helpers import url_for
from flask_login import login_required, current_user
from werkzeug.wrappers.response import Response
from PIL import Image
from psycopg2.errors import UniqueViolation

from os import path, remove
import uuid

from env_var import IMAGES_FOLDER, THUMBS_FOLDER
from .models import GalleryImage
from extensions import db

gallery = Blueprint("gallery", __name__)


@gallery.route("/images/<int:img_id>", methods=["GET"])
@login_required
def get_image_from_db(img_id: int) -> Response:
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
def delete_image_from_db(img_id: int) -> Response:

    image = GalleryImage.query.filter(
        GalleryImage.id == img_id, GalleryImage.user_id == current_user.id
    )
    remove(path.join(IMAGES_FOLDER, image.first().img_path))
    remove(path.join(THUMBS_FOLDER, image.first().thumb_path))
    image.delete()
    db.session.commit()
    return redirect(url_for("gallery.view_gallery"))


@gallery.route("/thumbs/<int:img_id>", methods=["GET"])
@login_required
def get_thumb_from_db(img_id: int) -> Response:

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
def upload() -> Response:
    def create_uuid(ext: str) -> tuple[str, str]:
        return f"{str(uuid.uuid4())}.{ext}", f"{str(uuid.uuid4())}.{ext}"

    for file in request.files.getlist("photo"):

        filename: str = file.filename  # type: ignore
        ext = filename.split(".")[1]
        ext = ext if ext != "jpg" else "jpeg"
        image = Image.open(file)
        img_height = image.height
        img_width = image.width
        image.thumbnail(size=(250, 250))
        thumb_height = image.height
        thumb_width = image.width

        while True:
            image_path, thumb_path = create_uuid(ext)
            image_to_save = GalleryImage(
                img_name=filename,
                img_path=image_path,
                thumb_path=thumb_path,
                img_width=img_width,
                img_height=img_height,
                thumb_height = thumb_height,
                thumb_width = thumb_width,
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
def view_gallery() -> str:
    images = GalleryImage.query.filter(GalleryImage.user_id == current_user.id).all()
    return render_template("index.html", images=images, username=current_user.username)
