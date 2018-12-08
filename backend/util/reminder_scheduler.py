import functools
import schedule
import time
from datetime import datetime, timedelta

from backend.app.database import db_session, ReminderEvents, ReminderLog


def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
        return result
    return wrapper


def add_reminder_to_log(id):
    rl = ReminderLog(reminder=id, executed_at=datetime.now())
    db_session.add(rl)
    db_session.commit()


def check_and_execute_reminder(last_executed, now, reminder, seconds):
    if not last_executed.executed_at > now - timedelta(seconds=seconds):
        add_reminder_to_log(reminder.id)


@with_logging
def check_reminders():
    reminders = (db_session.query(ReminderEvents)
                 .order_by(ReminderEvents.date_added.desc())
                 .all())

    now = datetime.now()
    current_time = now.time()
    previous_time = (now - timedelta(minutes=1)).time()
    for reminder in reminders:
        time_of_reminder = datetime.strptime(reminder.time_of_reminder, '%H:%M').time()
        if time_of_reminder > previous_time and time_of_reminder < current_time:
            last_executed = (db_session.query(ReminderLog)
                                .filter(ReminderLog.reminder == reminder.id)
                                .order_by(ReminderLog.executed_at.desc())
                                .first())
            print(reminder)
            if last_executed is None:
                add_reminder_to_log(reminder.id)
            else:
                if reminder.how_often.code == 'daily':
                    check_and_execute_reminder(last_executed, now, reminder, 60)
                elif reminder.how_often.code == 'hourly':
                    check_and_execute_reminder(last_executed, now, reminder, 60*60)
                elif reminder.how_often.code == 'weekly':
                    check_and_execute_reminder(last_executed, now, reminder, 60*60*24*7)
                else:
                    pass


if __name__ == '__main__':
    schedule.every(5).seconds.do(check_reminders)

    while 1:
        schedule.run_pending()