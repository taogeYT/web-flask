from flask import Flask
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from config import config
from datetime import datetime
db = SQLAlchemy()

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if not isinstance(obj, (list, dict, datetime)):
            return obj.__str__()
        else:
            return JSONEncoder.default(self, obj)

def create_app(config_name):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    from app.middleware import logined_user
    app.before_request_funcs.setdefault(None, []).append(logined_user)
    from app.main.page import page
    app.register_blueprint(page)
    from app.main.api import api
    app.register_blueprint(api)
    return app
