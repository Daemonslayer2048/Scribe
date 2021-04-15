from flask_login import current_user, login_user, logout_user, login_required
from flask import redirect, url_for
from . import Device, Repo, Device_Model, User
from . import home_bp
from . import db
from . import LoginForm, SignupForm
import flask

@login_required
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

@login_required
@home_bp.route("signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                username=form.name.data,
                email=form.email.data,
            )
        if len(User.query.all()) == 0:
            user.group = 1
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()  # Create new user
        login_user(user)  # Log in as newly created user
        return flask.redirect(url_for("home_bp.home"))
    flask.flash("A user already exists with that email address.")
    return flask.render_template(
        "signup.html",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )


@home_bp.route("logout")
def logout():
    logout_user()
    return flask.redirect(flask.url_for("user_bp.home"))


@login_required
@home_bp.route("web", methods=["GET", "POST"])
def home():
    if flask.request.method == "POST":
        if flask.request.form.get("enable_device"):
            device = flask.request.form.get("enable_device")
            query = (
                db.session.query(Device)
                .filter(Device.alias == device)
                .update({"enabled": True})
            )
            db.session.commit()
        elif flask.request.form.get("disable_device"):
            device = flask.request.form.get("disable_device")
            query = (
                db.session.query(Device)
                .filter(Device.alias == device)
                .update({"enabled": False})
            )
            db.session.commit()
        else:
            pass
    devices = (
        db.session.query(Device, Repo, Device_Model)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.model == Device_Model.id)
        .all()
    )
    return flask.render_template("home.html", devices=devices)


@login_required
@home_bp.route("")
def base():
    return redirect(url_for("home_bp.home"))
