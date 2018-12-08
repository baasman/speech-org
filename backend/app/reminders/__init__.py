from flask import Blueprint

reminders = Blueprint('reminders', __name__)

from . import views
