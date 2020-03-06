import connexion
from flask import Flask
from Scribe.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = connexion.FlaskApp(__name__, specification_dir="../api")
app.add_api("swagger.yaml")
app = app.app
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes, models
