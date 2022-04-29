from app import db
from flask_login import UserMixin


class GalleryImage(db.Model):
    """ Model for the table with images """

    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    img_filename = db.Column(db.String())
    img_width = db.Column(db.Integer())
    img_height = db.Column(db.Integer())
    img_data = db.Column(db.LargeBinary)
    img_thumb = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<image id={},name={}>'.format(self.id, self.name)


class User(UserMixin, db.Model):
    """ Model for the table with users """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(1000))
    images = db.relationship("GalleryImage")
