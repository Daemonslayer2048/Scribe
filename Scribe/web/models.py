from . import db

class device(db.Model):
    __tablename__ = "devices"
    pk = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(15), unique=True, nullable=False)
    port = db.Column(db.Integer, unique=True, nullable=False, default=22)
    alias = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), db.ForeignKey('device_models.pk'), nullable=False)
    user = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    enable = db.Column(db.String(120), nullable=True)
    last_updated = db.Column(db.String(32), nullable=False, default="Never")
    enabled = db.Column(db.Boolean, nullable=False)
    repo = db.Column(db.String(120), db.ForeignKey('repos.repo_name'), nullable=False, default="Default")
    proxy = db.Column(db.String(120), db.ForeignKey('proxies.alias'), nullable=True)

    def __repr__(self):
        return '<device {}>'.format(self.username)

class repo(db.Model):
    __tablename__ = "repos"
    pk = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return '<Repo {}>'.format(self.username)

class device_model(db.Model):
    __tablename__ = "device_models"
    pk = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    os = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Device_Model {}>'.format(self.username)

class proxy(db.Model):
    __tablename__ = "proxies"
    pk = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(120), nullable=False, unique=True)
    ip = db.Column(db.String(15), nullable=False)
    port = db.Column(db.Integer, nullable=False, default=22)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Proxy {}>'.format(self.username)

class user(db.Model):
    __tablename__ = "users"
    pk = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    group = db.Column(db.String(64), db.ForeignKey('groups.groupname'))
    password_hash = db.Column(db.String(128), unique=True, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class group(db.Model):
    __tablename__ = "groups"
    pk = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return '<Group {}>'.format(self.username)

class device_associations(db.Model):
    __tablename__ = "device_associations"
    pk = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(120), db.ForeignKey('devices.alias'))
    user = db.Column(db.String(64), db.ForeignKey('users.username'))
    group = db.Column(db.String(64), db.ForeignKey('groups.groupname'))

    def __repr__(self):
        return '<Device_Associations {}>'.format(self.username)
