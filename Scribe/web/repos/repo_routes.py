from flask_login import current_user, login_user, logout_user, login_required
import flask
from . import repo_bp
from . import db
from . import Repo, Device, Device_model

@repo_bp.route("/")
@login_required
def home():
    repos = Repo.query.all()
    return flask.render_template("repos.html", repos=repos)

@repo_bp.route("<repo>")
@login_required
def web_repo_devices(repo):
    devices = (db.session.query(Repo, Device, Device_model)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.model == Device_model.id)
        .filter(Repo.repo_name == str(repo))
        .all())
    return flask.render_template("repo.html", devices=devices)
