import flask
from . import groups_bp
from . import db
from . import Group

@groups_bp.route("/")
def web_groups():
    groups = Group.query.all()
    print(str(groups))
    return flask.render_template("groups.html", groups=groups)
