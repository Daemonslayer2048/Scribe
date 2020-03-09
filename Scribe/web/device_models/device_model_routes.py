from flask_login import current_user, login_user, logout_user, login_required
import flask
from . import device_model_bp
from . import db
from . import Device_model


@device_model_bp.route("/")
@login_required
def home():
    models = Device_model.query.all()
    return flask.render_template("device_model.html", models=models)
