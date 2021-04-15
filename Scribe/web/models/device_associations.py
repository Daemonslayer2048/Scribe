from . import db


class Device_Associations(db.Model):
    __tablename__ = "device_associations"
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(120), db.ForeignKey("devices.alias"))
    user = db.Column(db.String(64), db.ForeignKey("users.username"))
    group = db.Column(db.String(64), db.ForeignKey("groups.groupname"))

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Device_Associations {}>".format(self.username)
