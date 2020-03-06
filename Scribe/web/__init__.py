import connexion

app = connexion.FlaskApp(__name__, specification_dir="../api")
app.add_api("swagger.yaml")
app = app.app

from web import routes
