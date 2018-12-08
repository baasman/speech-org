from flask import Flask

from backend.app.database import db_session
from backend.config import app_config


def create_app(config='development'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config])

    from backend.app.reminders import reminders as reminder_blueprint
    app.register_blueprint(reminder_blueprint)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app