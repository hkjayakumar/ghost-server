import datetime
from typing import List

from flask import Blueprint, jsonify, request
from flask import g

from extensions import auth, db
from helper_responses import bad_request, Error
from models import LoginModel, UserModel, MessageModel

message_api = Blueprint('message_api', __name__)


@message_api.route('/api/v1/messages', methods=['POST'])
@auth.login_required
def new_message():