from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    """ Model for the table with users """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(1000))
    images = db.relationship("GalleryImage")
