from flask_login import current_user, login_user, logout_user, login_required
import flask
from . import group_bp
from . import db
from . import Group


@group_bp.route("/")
@login_required
def home():
    groups = Group.query.all()
    print(str(groups))
    return flask.render_template("groups.html", groups=groups)
