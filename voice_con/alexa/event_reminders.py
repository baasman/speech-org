from backend.app.database import db_session, ReminderSticky, ReminderEvents

from flask import Blueprint, render_template
from flask import current_app as capp
from flask_ask import Ask, question, statement, session


blueprint = Blueprint('event_reminders', __name__, url_prefix="/")
ask = Ask(blueprint=blueprint)

## Event reminder CRUD

@ask.launch
def startup():
    welcome_msg = render_template('welcome')
    capp.logger.info(session.user.userId)
    print(session.user.userId)
    return question(welcome_msg)


@ask.intent('ReminderEventDoneIntent', convert={'id': int})
def event_reminder_complete(id):
    try:
        r = db_session.query(ReminderEvents).filter(ReminderEvents.id == id).first()
        r.completed_since_last = True
        db_session.commit()
        return statement(render_template('reminder_completed'))
    except:
        return statement('Unable to find reminder {}'.format(id))


@ask.intent('ReminderEventRemoveIntent', convert={'id': int})
def event_reminder_remove(id):
    try:
        r = db_session.query(ReminderEvents).filter(ReminderEvents.id == id).first()
        db_session.delete(r)
        db_session.commit()
        return statement(render_template('reminder_removed'))
    except:
        return statement('Unable to find reminder {}'.format(id))


@ask.intent('ReadPriorityRemindersIntent')
def read_priority_reminders(id):
    try:
        r = db_session.query(ReminderEvents).filter(ReminderEvents.id == id).first()
        db_session.delete(r)
        db_session.commit()
        return statement(render_template('reminder_removed'))
    except:
        return statement('Unable to find reminder {}'.format(id))

@ask.session_ended
def session_ended():
    return "{}", 200
