from backend.database import (
    db_session,
    ReminderSticky,
    ReminderEvents,
    User
)

import random

from faker import Faker


def generate_random_datetime():
    hour = "%02d" % random.randint(0, 23)
    minute = "%02d" % random.randint(1, 59)
    time = '{}:{}'.format(hour, minute)
    return time

def generate_how_often():
    return random.choice(ReminderEvents.TYPES)[0]

def insert_data(n_users=10, n_sticky=5, n_events=10):
    fake = Faker()

    users = set([fake.name() for _ in range(n_users)])
    print(len(users))

    for user in users:
        u = User(username=user, password='pass123')
        for i in range(n_sticky):
            sticky = ReminderSticky(reminder=fake.text())
            u.reminders_sticky.append(sticky)
        for i in range(n_events):
            event = ReminderEvents(reminder=fake.text(),
                                   time_of_reminder=generate_random_datetime(),
                                   how_often=generate_how_often())
            u.reminders_events.append(event)
        db_session.add(u)

        try:
            db_session.commit()
        except Exception as e:
            print(str(e))



if __name__ == '__main__':
    insert_data(20, 5, 10)