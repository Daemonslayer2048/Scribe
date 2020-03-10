from flask_login import current_user, login_user, logout_user, login_required
from . import Device, Repo, Device_model, User
from . import home_bp
from . import db
from . import LoginForm
import flask


@home_bp.route("login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("home_bp.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flask.flash("Invalid username or password")
            return flask.redirect(flask.url_for("home_bp.login"))
        login_user(user, remember=form.remember_me.data)
        return flask.redirect(flask.url_for("home_bp.home"))
    return flask.render_template("login.html", title="Sign In", form=form)


@home_bp.route("logout")
def logout():
    logout_user()
    return flask.redirect(flask.url_for("user_bp.home"))


@home_bp.route("web")
@login_required
def home():
    devices = (
        db.session.query(Device, Repo, Device_model)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.model == Device_model.id)
        .all()
    )
    return flask.render_template("home.html", devices=devices)
