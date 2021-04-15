from . import db


class Proxy(db.Model):
    __tablename__ = "proxies"
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(120), nullable=False, unique=True)
    ip = db.Column(db.String(15), nullable=False)
    port = db.Column(db.Integer, nullable=False, default=22)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Proxy {}>".format(self.alias)
