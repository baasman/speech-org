from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Boolean
)
from sqlalchemy_utils.types.choice import ChoiceType
from flask_login import UserMixin

from datetime import datetime
from backend.config import app_config


url = app_config['development'].SQLALCHEMY_DATABASE_URI
engine = create_engine(url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(), unique=False, nullable=False)
    reminders_sticky = relationship('ReminderSticky')
    reminders_events = relationship('ReminderEvents')
    alexa_user_id = Column(String, unique=True, nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class ReminderSticky(Base):
    __tablename__ = 'reminders_sticky'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), ForeignKey('users.username'), nullable=False)
    reminder = Column(String(120))
    completed = Column(Boolean(), default=False)
    priority = Column(Boolean(), default=False)
    date_added = Column(DateTime(), default=datetime.now())
    importance = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return '<Reminder {}, {}>'.format(self.username, self.reminder)


class ReminderEvents(Base):
    TYPES = [
        ('daily', 'Daily'),
        ('hourly', 'Hourly'),
        ('weekly', 'Weekly'),
    ]
    __tablename__ = 'reminders_events'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), ForeignKey('users.username'), nullable=False)
    reminder = Column(String())
    time_of_reminder = Column(String(), nullable=True)
    how_often = Column(ChoiceType(TYPES))
    date_added = Column(DateTime(), default=datetime.now())
    completed_since_last = Column(Boolean(), default=False)

    def __repr__(self):
        return '<ReminderEvent {}, {}, {}>'.format(self.username, self.reminder,
                                               self.time_of_reminder)


class ReminderLog(Base):
    __tablename__ = 'reminder_log'
    id = Column(Integer, primary_key=True)
    reminder = Column(Integer, ForeignKey('reminders_events.id'), nullable=False)
    executed_at = Column(DateTime(), nullable=False)

    def __repr__(self):
        return '<ReminderLog {}, {}>'.format(self.reminder, self.executed_at)


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
    # u = User(username='leah')
    # rem = ReminderSticky(reminder='take out trash')
    # rem2 = ReminderEvents(reminder='clean dishes', time_based=True,
    #                 time_of_reminder='10:02', how_often='daily')
    # u.reminders_sticky.append(rem)
    # u.reminders_events.append(rem2)
    # db_session.add(u)
    # db_session.commit()

