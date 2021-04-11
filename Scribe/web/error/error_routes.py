from . import error_bp
from . import db
import flask


@error_bp.route("", methods=["GET", "POST"])
def setup():
    return flask.render_template("setup.html")
