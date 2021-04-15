from flask_login import current_user, login_user, logout_user, login_required
from ..lib import git, repos, models, devices
from . import NewDeviceForm
from . import device_bp
import flask


@device_bp.route("/config/<alias>")
@login_required
def config(alias):
    config = str(devices.get_config(str(alias)))
    config = config.split("\n")
    logs = git.get_device_git_log(alias)
    repo = repos.get_device_repo(alias)
    model = models.get_devices_model(alias)
    return flask.render_template(
        "config.html", repo=repo, model=model, alias=alias, config=config, logs=logs
    )

@device_bp.route("/new_device", methods=["GET", "POST"])
@login_required
def new_device():
    return flask.render_template(
        "new_device.jinja2"
    )
