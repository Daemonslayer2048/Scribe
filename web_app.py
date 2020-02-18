#! /usr/bin/python3
import api
import db
import flask
import os
import connexion

app = connexion.App(__name__, specification_dir="./api")
app.add_api("swagger.yaml")

#############
# Home URLs #
#############
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
    return flask.render_template("config.html", config=config)


if __name__ == "__main__":
    if not os.path.exists("./Scribe.db"):
        print("Building Database")
        db.build_db()
    app.run()
