from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    from app.main.page import page
    app.register_blueprint(page)
    from app.main.api import api
    app.register_blueprint(api)
    return app
