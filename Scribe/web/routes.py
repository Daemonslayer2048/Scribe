#! python3
from . import app
from Scribe import api
from Scribe.web import db
from .forms import LoginForm
import flask
import os


#############
# Home URLs #
#############
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flask.flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return flask.redirect(flask.url_for('home'))
    return flask.render_template('login.html', title='Sign In', form=form)

@app.route("/web")
def home():
    devices = api.devices.get()
    for device in devices:
        device.update({"model": api.models.get_devices_model(device["alias"])["model"]})
    return flask.render_template("home.html", devices=devices)


###############
# Users URLs  #
###############
@app.route("/web/users")
def users():
    users = api.users.get()
    return flask.render_template("users.html", users=users)


###############
# Groups URLs #
###############
@app.route("/web/groups")
def groups():
    groups = api.groups.get()
    return flask.render_template("groups.html", groups=groups)


###############
# Models URLs #
###############
@app.route("/web/models")
def models():
    models = api.models.get()
    return flask.render_template("models.html", models=models)


##############
# Repos URLs #
##############
@app.route("/web/repos")
def repos():
    repos = api.repos.get()
    return flask.render_template("repos.html", repos=repos)


@app.route("/web/repos/<repo>")
def repo_devices(repo):
    devices = api.repos.get_repo_devices(repo)
    return flask.render_template("repo.html", devices=devices)


##############
# Other URLS #
##############
@app.route("/web/config/<alias>")
def config(alias):
    config = str(api.devices.get_config(str(alias)))
    config = config.split("\n")
    logs = api.git.get_device_git_log(alias)
    repo = api.repos.get_device_repo(alias)
    model = api.models.get_devices_model(alias)
    return flask.render_template("config.html", repo=repo, model=model, alias=alias, config=config, logs=logs)
