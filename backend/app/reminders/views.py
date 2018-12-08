from flask import jsonify, request

from backend.app.database import db_session, ReminderSticky, ReminderEvents
from . import reminders


@reminders.route('/reminders/<user>', methods=['GET'])
def check_reminders(user):
    reminders = (db_session.query(ReminderSticky)
                    .filter(ReminderSticky.username == user)
                    .order_by(ReminderSticky.date_added.desc())
                    .all())
    reminders = [i.reminder for i in reminders]
    return jsonify({'user': user, 'reminders': reminders})


@reminders.route('/reminders/<id>/priority', methods=['PUT'])
def set_priority(id):
    (db_session.query(ReminderSticky)
        .filter(ReminderSticky.id == id)
        .update({'priority': True}))
    return jsonify({'id': id})


@reminders.route('/reminders/add/sticky/<user>', methods=['POST'])
def add_sticky_reminder(user):
    message = request.args['reminder']
    new_reminder = ReminderSticky(username=user, reminder=message)
    db_session.add(new_reminder)
    db_session.commit()
    return jsonify({'message': message})


@reminders.route('/reminders/add/reoccurring/<user>', methods=['POST'])
def add_reoccurring_reminder(user):
    message = request.args['reminder']
    time = request.args['daily_time']
    how_often = request.args['how_often']
    new_reminder = ReminderEvents(username=user, reminder=message,
                                  time_of_reminder=time, time_based=True,
                                  how_often=how_often)
    db_session.add(new_reminder)
    db_session.commit()
    return jsonify({'message': message})


@reminders.route('/reminders/remove/sticky/<id>', methods=['DELETE'])
def remove_sticky_reminder(id):
    db_session.query(ReminderSticky).filter(ReminderSticky.id == id).delete()
    db_session.commit()
    return jsonify({'id': id})


@reminders.route('/reminders/remove/event/<id>', methods=['DELETE'])
def remove_sticky_reminder(id):
    db_session.query(ReminderEvents).filter(ReminderEvents.id == id).delete()
    db_session.commit()
    return jsonify({'id': id})
