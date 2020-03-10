from flask_login import current_user, login_user, logout_user, login_required
import flask
from . import user_bp
from . import db
from . import User


@user_bp.route("/")
@login_required
def home():
    users = User.query.all()
    return flask.render_template("users.html", users=users)
