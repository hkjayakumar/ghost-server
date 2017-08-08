from app import factory

import os
from app import socketio

import events

ghost = factory(os.environ['APP_SETTINGS'])
socketio.init_app(ghost)
