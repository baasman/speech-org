from backend.database import db_session, ReminderSticky

from flask import Blueprint, render_template
from flask import current_app as capp
from flask_ask import Ask, question, statement, session


blueprint = Blueprint('sticky_reminders', __name__, url_prefix="/")
ask = Ask(blueprint=blueprint)

### Sticky reminder CRUD

@ask.launch
def startup():
    welcome_msg = render_template('welcome')
    capp.logger.info(session.user.userId)
    print(session.user.userId)
    return question(welcome_msg)


@ask.intent('ReminderStickyDoneIntent', convert={'id': int})
def sticky_reminder_complete(id):
    try:
        r = db_session.query(ReminderSticky).filter(ReminderSticky.id == id).first()
        r.completed = True
        db_session.commit()
        return statement(render_template('reminder_completed'))
    except:
        return statement('Unable to find reminder {}'.format(id))


@ask.intent('ReminderStickyRemoveIntent', convert={'id': int})
def sticky_reminder_remove(id):
    try:
        r = db_session.query(ReminderSticky).filter(ReminderSticky.id == id).first()
        db_session.delete(r)
        db_session.commit()
        return statement(render_template('reminder_removed'))
    except:
        return statement('Unable to find reminder {}'.format(id))


@ask.intent('ReminderStickySetPriorityIntent', convert={'id': int})
def sticky_reminder_remove(id):
    try:
        r = db_session.query(ReminderSticky).filter(ReminderSticky.id == id).first()
        r.priority = True
        db_session.commit()
        return statement(render_template('set_priority'))
    except:
        return statement('Unable to find reminder {}'.format(id))

@ask.session_ended
def session_ended():
    return "{}", 200
