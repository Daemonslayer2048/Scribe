from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True, nullable=False)
    port = db.Column(db.Integer, nullable=False, default=22)
    alias = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), db.ForeignKey("device_models.id"), nullable=False)
    user = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    enable = db.Column(db.String(120), nullable=True)
    last_updated = db.Column(db.String(32), nullable=False, default="Never")
    enabled = db.Column(db.Boolean, nullable=False)
    repo = db.Column(
        db.String(120),
        db.ForeignKey("repos.repo_name"),
        nullable=False,
        default="Default",
    )
    proxy = db.Column(db.String(120), db.ForeignKey("proxies.alias"), nullable=True)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Device {}>".format(self.alias)
