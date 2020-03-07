import flask
from . import repo_bp
from . import db
from . import Repo, Device, Device_model

@repo_bp.route("/")
def repos():
    repos = Repo.query.all()
    return flask.render_template("repos.html", repos=repos)

@repo_bp.route("<repo>")
def web_repo_devices(repo):
    devices = (db.session.query(Repo, Device, Device_model)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.model == Device_model.id)
        .filter(Repo.repo_name == str(repo))
        .all())
    return flask.render_template("repo.html", devices=devices)
