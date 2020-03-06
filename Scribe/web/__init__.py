import connexion
from flask import Flask
from Scribe.config import Config

app = connexion.FlaskApp(__name__, specification_dir="../api")
app.add_api("swagger.yaml")
app = app.app
app.config.from_object(Config)

from . import routes
