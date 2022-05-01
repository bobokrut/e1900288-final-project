from flask import request, redirect, abort, Blueprint, render_template, Response
from flask.helpers import url_for
from flask_login import login_required, current_user
from .models import GalleryImage
from PIL import Image
from io import BytesIO
from extensions import db

gallery = Blueprint("gallery", __name__)


@gallery.route('/images/<int:img_id>', methods=['GET'])
@login_required
def get_image_from_db(img_id):
    image = GalleryImage.query.filter(GalleryImage.id == img_id, GalleryImage.user_id == current_user.id).with_entities(GalleryImage.img_data).first()
    if image:
        return Response(image[0], mimetype='application/octet-stream')
    abort(404)


@gallery.route('/images/<int:img_id>', methods=["POST"])
@login_required
def delete_image_from_db(img_id):

    GalleryImage.query.filter(GalleryImage.id==img_id, GalleryImage.user_id == current_user.id).delete()
    db.session.commit()
    return redirect(url_for("gallery.view_gallery"))


@gallery.route('/thumbs/<int:img_id>', methods=['GET'])
@login_required
def get_thumb_from_db(img_id):
    image = GalleryImage.query.filter(GalleryImage.id == img_id, GalleryImage.user_id == current_user.id).with_entities(GalleryImage.img_thumb).first()
    if image:
        return Response(image[0], mimetype='application/octet-stream')

    abort(404)


@gallery.route('/upload', methods=["POST"])
@login_required
def upload():
    for file in request.files.getlist("photo"):

        filename = file.filename
        ext = filename.split(".")[1]
        ext = ext if ext != "jpg" else "jpeg"
        blob = file.read()

        # start of the thumbnail creation
        image = Image.open(file)
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


@gallery.route("/")
@login_required
def view_gallery():
    images = GalleryImage.query.filter(GalleryImage.user_id == current_user.id).with_entities(GalleryImage.id, GalleryImage.img_width, GalleryImage.img_height).all()
    return render_template("index.html", images=images, username=current_user.username)
