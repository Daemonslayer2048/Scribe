from . import db


class Group_Associations(db.Model):
    __tablename__ = "group_associations"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Group Associations {}>".format(self.username)
