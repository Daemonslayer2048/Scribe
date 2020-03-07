import flask
from . import group_bp
from . import db
from . import Group

@group_bp.route("/")
def web_groups():
    groups = Group.query.all()
    print(str(groups))
    return flask.render_template("groups.html", groups=groups)
