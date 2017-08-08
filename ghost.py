from app import factory

import os
from flask_socketio import SocketIO
from app import socketio

import events

ghost = factory(os.environ['APP_SETTINGS'])
socketio.init_app(ghost)
socketio.run(ghost)
