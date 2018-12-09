from flask import Flask

from backend.database import db_session


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app