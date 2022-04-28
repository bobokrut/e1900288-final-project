from pathlib import Path
from models import GalleryImage
from flask_login import current_user

resources = Path(__file__).parent / "files"


def test_image_upload(client_without_images):
    before = GalleryImage.query.filter(GalleryImage.img_filename == "pexels-pixabay-302743.jpg", GalleryImage.user_id == current_user.id).with_entities(GalleryImage.id).all()

    response = client_without_images.post("/upload", follow_redirects=True, data={
        "photo": ((resources / "pexels-pixabay-302743.jpg").open("rb"), "pexels-pixabay-302743.jpg")
    })
    after = GalleryImage.query.filter(GalleryImage.img_filename == "pexels-pixabay-302743.jpg", GalleryImage.user_id == current_user.id).with_entities(GalleryImage.id).all()

    assert response.status_code == 200
    assert len(before) + 1 == len(after)
    assert len(after) == 1
    assert after[0]
    assert response.request.path == "/"


def test_get_image(client_with_image):
    image_id = GalleryImage.query.filter(GalleryImage.img_filename == "pexels-pixabay-302743.jpg", GalleryImage.user_id == current_user.id).with_entities(GalleryImage.id).first()[0]
    response = client_with_image.get(f"/images/{image_id}")
    assert response.status_code == 200


def test_get_thumbnail(client_with_image):
    image_id = GalleryImage.query.filter(GalleryImage.img_filename == "pexels-pixabay-302743.jpg", GalleryImage.user_id == current_user.id).with_entities(GalleryImage.id).first()[0]
    response = client_with_image.get(f"/thumbs/{image_id}")
    assert response.status_code == 200
