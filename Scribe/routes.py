#! python3
# from flask_login import current_user, login_user, logout_user, login_required
from shared import devices, git, repos, models
from web.models import User, Group, Device_model, Repo, Device
from web import app
from web import db
from web.forms import LoginForm
import flask
import os


#############
# Home URLs #
#############
@app.route("/login", methods=["GET", "POST"])
def web_login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("web_home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flask.flash("Invalid username or password")
            return flask.redirect(flask.url_for("web_login"))
        login_user(user, remember=form.remember_me.data)
        return flask.redirect(flask.url_for("web_home"))
    return flask.render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def web_logout():
    logout_user()
    return flask.redirect(flask.url_for("index"))


@app.route("/web")
@login_required
def web_home():
    devices = (
        db.session.query(Device, Repo, Device_model)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.model == Device_model.id)
        .all()
    )
    return flask.render_template("home.html", devices=devices)


###############
# Users URLs  #
###############
@app.route("/web/users")
@login_required
def web_users():
    users = User.query.all()
    return flask.render_template("users.html", users=users)


###############
# Groups URLs #
###############
@app.route("/web/groups")
@login_required
def web_groups():
    groups = Group.query.all()
    return flask.render_template("groups.html", groups=groups)


###############
# Models URLs #
###############
@app.route("/web/models")
@login_required
def web_models():
    models = Device_model.query.all()
    return flask.render_template("models.html", models=models)


##############
# Repos URLs #
##############
@app.route("/web/repos")
@login_required
def web_repos():
    repos = Repo.query.all()
    return flask.render_template("repos.html", repos=repos)


@app.route("/web/repos/<repo>")
@login_required
def web_repo_devices(repo):
    devices = (
        db.session.query(Repo, Device, Device_model)
        .filter(Device.repo == Repo.repo_name)
        .filter(Device.model == Device_model.id)
        .filter(Repo.repo_name == str(repo))
        .all()
    )
    return flask.render_template("repo.html", devices=devices)


##############
# Other URLS #
##############
@app.route("/web/config/<alias>")
@login_required
def web_config(alias):
    config = str(devices.get_config(str(alias)))
    config = config.split("\n")
    logs = git.get_device_git_log(alias)
    repo = repos.get_device_repo(alias)
    model = models.get_devices_model(alias)
    return flask.render_template(
        "config.html", repo=repo, model=model, alias=alias, config=config, logs=logs
    )
