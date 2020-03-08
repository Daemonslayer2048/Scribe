from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db
from . import login

class Device(db.Model):
    __tablename__ = "devices"
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True, nullable=False)
    port = db.Column(db.Integer, nullable=False, default=22)
    alias = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), db.ForeignKey('device_models.id'), nullable=False)
    user = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    enable = db.Column(db.String(120), nullable=True)
    last_updated = db.Column(db.String(32), nullable=False, default="Never")
    enabled = db.Column(db.Boolean, nullable=False)
    repo = db.Column(db.String(120), db.ForeignKey('repos.repo_name'), nullable=False, default="Default")
    proxy = db.Column(db.String(120), db.ForeignKey('proxies.alias'), nullable=True)

    def __repr__(self):
        return '<Device {}>'.format(self.alias)

class Repo(db.Model):
    __tablename__ = "repos"
    id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return '<Repo {}>'.format(self.repo_name)

class Device_model(db.Model):
    __tablename__ = "device_models"
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    os = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Device_Model {}>'.format(self.id)

class Proxy(db.Model):
    __tablename__ = "proxies"
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(120), nullable=False, unique=True)
    ip = db.Column(db.String(15), nullable=False)
    port = db.Column(db.Integer, nullable=False, default=22)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Proxy {}>'.format(self.alias)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    group = db.Column(db.String(64), db.ForeignKey('groups.groupname'))
    password_hash = db.Column(db.String(128), unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return '<Group {}>'.format(self.groupname)

class Device_associations(db.Model):
    __tablename__ = "device_associations"
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(120), db.ForeignKey('devices.alias'))
    user = db.Column(db.String(64), db.ForeignKey('users.username'))
    group = db.Column(db.String(64), db.ForeignKey('groups.groupname'))

    def __repr__(self):
        return '<Device_Associations {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
