from . import db


class Repo(db.Model):
    __tablename__ = "repos"
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(120), nullable=False, unique=True)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Repo {}>".format(self.repo_name)
