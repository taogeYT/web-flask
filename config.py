import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    # JSONIFY_MIMETYPE = 'application/json;charset=utf-8'
    COOKIE_NAME = 'dsn'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    # SQLALCHEMY_DATABASE_URI = 'oracle://lyt:lyt@local:1521/xe'
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@local:3306/test?charset=utf8"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
