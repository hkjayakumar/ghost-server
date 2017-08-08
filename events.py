from flask_socketio import send,emit

from ghost import socketio

import datetime
from typing import List

from flask import g, jsonify, request

from extensions import auth, db
from helper_responses import bad_request, Error
from models import LoginModel, UserModel

userToSocket = {}

@socketio.on('connect')
def connect():
    user_id = request.args.get('user_id') # Type:int
    token = request.args.get('token')

    print("HEREEEEEEEEE")

    user = UserModel.query.filter(UserModel.id == user_id).first()  # type:UserModel
    if user is None:
        emit('exception', 'User with id ' + str(user_id) + ' not found')

    login = LoginModel.verify_auth_token(token)
    if not login:
        emit('exception', 'Invalid Auth Token')

    g.login = login  # type: LoginModel    
    user = g.login.user  # type: UserModel
    if user_id != user.id:
        emit('exception', 'No permission to connect as ' + str(user_id))

    userToSocket[user_id] = request.sid

    # Check if there are any messages to be delivered to this user
    messagesQuery = MessageModel.query.filter(MessageModel.receiver_id == user_id) # type:MessageModelsQuery
    if messagesQuery.count() == 0:
        emit('established')
    else:
        messages = messagesQuery.all() # type:List[MessageModels]
        messages = [m.to_dict() for m in messages]
        emit('messages', jsonify('messages': messages))


@socketio.on('disconnect')
def disconnect():
    session_id = request.sid
    for k,v in userToSocket.items():
        if v == session_id:
            del userToSocket[k]


@socketio.on('message_send')
def message(message):
    sender_id = request.args.get('sender_id') # Type:int
    token = request.args.get('token')

    user = UserModel.query.filter(UserModel.id == sender_id).first()  # type:UserModel
    if user is None:
        emit('exception', 'User with id ' + str(sender_id) + ' not found')

    login = LoginModel.verify_auth_token(token)
    if not login:
        emit('exception', 'Invalid Auth Token')

    g.login = login  # type: LoginModel    
    user = g.login.user  # type: UserModel
    if sender_id != user.id:
        emit('exception', 'No permission to connect as ' + str(sender_id))


    if receiver_id in userToSocket:
        emit('message_send', jsonify('message': message), room=userToSocket[receiver_id])
    else:
        # Store in Database
        emit('stored')