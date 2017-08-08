import datetime
from typing import List

from flask import Blueprint, jsonify, request
from flask import g

from extensions import auth, db
from helper_responses import bad_request, Error
from models import LoginModel, UserModel, MessageModel
from utils import date_time_from_str

message_api = Blueprint('message_api', __name__)


@message_api.route('/api/v1/messages', methods=['POST'])
@auth.login_required
def send_message():
    sender_id = request.json.get('sender_id')  # type:int
    receiver_id = request.json.get('receiver_id')  # type:int
    message_ciphertext = request.json.get('message') # type:str
    timestamp = request.json.get('timestamp') # type:str

    if any(x is None for x in [sender_id, receiver_id, message_ciphertext, timestamp]):
        return bad_request(Error.MISSING_ARGS)

    login_model = g.login  # type: LoginModel
    if sender_id != login_model.user_id:
        return bad_request(Error.ILLEGAL_ARGS, 'No permission to send as user ' + str(sender_id))

    try:
        timestamp = date_time_from_str(timestamp)  # type:datetime
    except (IndexError, AttributeError):
        return bad_request(Error.ILLEGAL_ARGS, 'Malformed timestamp')

    message = MessageModel(sender_id=sender_id, receiver_id=receiver_id, 
        message_ciphertext=message_ciphertext, timestamp=timestamp)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': message.to_dict(), 'error': None}), 201


@message_api.route('/api/v1/messages/<int:user_id>', methods=['GET'])
@auth.login_required
def receive_message(user_id: int):
    user = UserModel.query.filter(UserModel.id == user_id).first()  # type:UserModel
    if user is None:
        return bad_request(Error.ILLEGAL_ARGS, 'User with id ' + str(user_id) + ' not found')

    login_model = g.login  # type: LoginModel
    user = login_model.user  # type: UserModel

    if user_id != user.id:
        return bad_request(Error.ILLEGAL_ARGS, 'No permission to get user messages ' + str(user_id))

    messageRecords = MessageModel.query.filter(MessageModel.receiver_id == user_id).all()  # type:List[SkillModel]
    messages = [m.to_dict() for m in messageRecords]
    
    for m in messageRecords:
        db.session.delete(m)
    db.session.commit()
    
    return jsonify({'messages': messages, 'error': None}), 201