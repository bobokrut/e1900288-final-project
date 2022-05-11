from pathlib import Path
from gallery.models import GalleryImage
from flask_login import current_user
from flask.testing import FlaskClient

import os

from env_var import IMAGES_FOLDER, THUMBS_FOLDER

resources = Path(__file__).parent / "files"


def test_image_upload(client_without_images: FlaskClient) -> None:
    db_before = (
        GalleryImage.query.filter(
            GalleryImage.user_id == current_user.id,
        )
        .with_entities(GalleryImage.id)
        .all()
    )
    images_in_folder_before = len(os.listdir(IMAGES_FOLDER))
    thumbs_in_folder_before = len(os.listdir(THUMBS_FOLDER))

    response = client_without_images.post(
        "/upload",
        follow_redirects=True,
        data={
            "photo": (
                (resources / "pexels-pixabay-302743.jpg").open("rb"),
                "pexels-pixabay-302743.jpg",
            )
        },
    )
    db_after = (
        GalleryImage.query.filter(
            GalleryImage.user_id == current_user.id,
        )
        .with_entities(GalleryImage.id)
        .all()
    )

    image_response = client_without_images.get(f"/images/{db_after[-1][0]}")
    thumb_response = client_without_images.get(f"/thumbs/{db_after[-1][0]}")
    images_in_folder_after = len(os.listdir(IMAGES_FOLDER))
    thumbs_in_folder_after = len(os.listdir(THUMBS_FOLDER))

    assert response.status_code == 200
    assert image_response.status_code == 200
    assert thumb_response.status_code == 200
    assert len(db_before) + 1 == len(db_after)
    assert images_in_folder_before + 1 == images_in_folder_after
    assert thumbs_in_folder_before + 1 == thumbs_in_folder_after
    assert response.request.path == "/"
