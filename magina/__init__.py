from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()


def create_app(config_name: str):
    app = Flask(__name__)

    # configuration
    app.jinja_env.auto_reload = True
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'default.login'

    from . import models
    db.create_all(app=app)

    from .default import blueprint
    app.register_blueprint(blueprint)

    return app
