#!/usr/bin/python3
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__, instance_relative_config=False)
db = SQLAlchemy()
app.config.from_object("config.Config")
if app.config['INSTALLED'] == True:
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    login = LoginManager(app)
    login.login_view = "home_bp.login"
    # Make sure needed groups exist
    from .models import Group
    if len(Group.query.all()) == 0:
        admin_group = Group(
            groupname = "Administrators"
        )
        db.session.add(admin_group)
        db.session.commit()
    with app.app_context():
        from .groups import group_routes
        from .device_models import device_model_routes
        from .users import user_routes
        from .repos import repo_routes
        from .home import home_routes
        from .devices import device_routes
        from .api import api_routes

        app.register_blueprint(group_routes.group_bp)
        app.register_blueprint(device_model_routes.device_model_bp)
        app.register_blueprint(user_routes.user_bp)
        app.register_blueprint(repo_routes.repo_bp)
        app.register_blueprint(home_routes.home_bp)
        app.register_blueprint(device_routes.device_bp)
        app.register_blueprint(api_routes.api_bp)
else:
    # You need to throw an error if the config does not exist
    with app.app_context():
        from .error import error_routes
        app.register_blueprint(error_routes.error_bp)
