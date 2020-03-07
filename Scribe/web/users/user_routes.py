import flask
from . import user_bp
from . import db
from . import User

@user_bp.route("/")
def home():
    users = User.query.all()
    return flask.render_template("users.html", users=users)
