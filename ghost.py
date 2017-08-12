import os

from app.app import factory
from app.app import socketio
import app.events

ghost = factory(os.environ['APP_SETTINGS'])
socketio.init_app(ghost)

if __name__ == '__main__':
    socketio.run(ghost)