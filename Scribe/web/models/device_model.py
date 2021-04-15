from . import db


class Device_Model(db.Model):
    __tablename__ = "device_models"
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    os = db.Column(db.String(120), nullable=False)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Device_Model {}>".format(self.id)
