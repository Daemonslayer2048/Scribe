import flask
from . import device_model_bp
from . import db
from . import Device_model

@device_model_bp.route("/")
def device_models():
    models = Device_model.query.all()
    return flask.render_template("device_model.html", models=models)
