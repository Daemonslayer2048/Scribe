from . import db


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(64), unique=True, nullable=False)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Group {}>".format(self.groupname)
