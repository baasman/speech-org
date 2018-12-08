import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DASHBOARD_PORT = 5001


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(basedir, 'test.db'))
    DASHBOARD_PORT = 5003


class TestingConfig(Config):
    TESTING = True
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False


app_config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
