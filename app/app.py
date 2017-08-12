import os

from flask import Flask
from app.api.user_api import user_api
from app.api.message_api import message_api

from app import config
from app.extensions import db

from flask_socketio import SocketIO
socketio = SocketIO()

def factory(configuration=config.DevelopmentConfig):
    application = Flask(__name__)
    application.config.from_object(configuration)
    db.init_app(application)
    application.register_blueprint(user_api)
    application.register_blueprint(message_api)
    
    @application.route('/api/v1/')
    def landing_page():
        return 'Welcome to Ghost API v1'

    return application