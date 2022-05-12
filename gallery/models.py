from extensions import db


class GalleryImage(db.Model):  # type: ignore
    """Model for the table with images"""

    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    img_width = db.Column(db.Integer)
    img_height = db.Column(db.Integer)
    thumb_width = db.Column(db.Integer)
    thumb_height = db.Column(db.Integer)
    img_path = db.Column(db.String, unique=True)
    thumb_path = db.Column(db.String, unique=True)

    def __repr__(self) -> str:
        return "<image id={},name={}>".format(self.id, self.name)
