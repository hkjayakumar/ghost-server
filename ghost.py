from app import factory

import os
from flask_socketio import SocketIO


ghost = factory(os.environ['APP_SETTINGS'])
socketio = SocketIO(ghost)
socketio.run(ghost)