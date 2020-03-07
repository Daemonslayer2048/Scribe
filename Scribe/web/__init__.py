from flask import Flask
#from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # Application Configuration
    app.config.from_object('config.Config')
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
#    login = LoginManager(app)
#    login.login_view = 'login'
    with app.app_context():
        from .groups import group_routes
        from .device_models import device_model_routes

        app.register_blueprint(group_routes.groups_bp)
        app.register_blueprint(device_model_routes.device_model_bp)
    return app
