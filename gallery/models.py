from extensions import db


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
