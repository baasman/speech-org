from flask import render_template
from flask import current_app as capp

from flask_ask import Ask, statement, question, session
from flask_ask import request as ask_request

from voice_con.alexa.create_app import create_app
from voice_con.alexa.config import app_config
from voice_con.alexa.sticky_reminders import blueprint as sticky_reminder_blueprint
from voice_con.alexa.event_reminders import blueprint as event_reminder_blueprint
from backend.app.database import db_session, ReminderSticky, ReminderEvents

import os

config_type = os.environ.get('FLASK_CONFIG1', 'development')

app = create_app(app_config[config_type])
app.register_blueprint(event_reminder_blueprint)
app.register_blueprint(sticky_reminder_blueprint)


if __name__ == '__main__':
    app.run(port=5004)

