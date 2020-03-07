import flask
from . import group_bp
from . import db
from . import Group

@group_bp.route("/")
def home():
    groups = Group.query.all()
    print(str(groups))
    return flask.render_template("groups.html", groups=groups)
