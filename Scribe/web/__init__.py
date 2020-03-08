from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=False)
db = SQLAlchemy()
app.config.from_object('config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'home_bp.login'
with app.app_context():
    from .groups import group_routes
    from .device_models import device_model_routes
    from .users import user_routes
    from .repos import repo_routes
    from .home import home_routes
    from .devices import device_routes
    app.register_blueprint(group_routes.group_bp)
    app.register_blueprint(device_model_routes.device_model_bp)
    app.register_blueprint(user_routes.user_bp)
    app.register_blueprint(repo_routes.repo_bp)
    app.register_blueprint(home_routes.home_bp)
    app.register_blueprint(device_routes.device_bp)
