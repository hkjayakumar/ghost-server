import datetime
from typing import List

from flask import Blueprint, jsonify, request
from flask import g

from app.extensions import auth, db
from app.utils import bad_request, Error
from app.models import LoginModel, UserModel

user_api = Blueprint('user_api', __name__)


@user_api.route('/api/v1/users', methods=['POST'])
def new_user():
    username = request.json.get('username')  # type:str
    password = request.json.get('password')  # type:str

    if any(x is None for x in [username, password]):
        return bad_request(Error.MISSING_ARGS)

    if LoginModel.query.filter_by(username=username).first() is not None:
        return bad_request(Error.ILLEGAL_ARGS, 'User already exists')

    user = UserModel(friends=[])
    db.session.add(user)
    db.session.flush()  # assigns id to user
    
    login = LoginModel(user_id=user.id, username=username)
    login.hash_password(password)
    db.session.add(login)
    
    db.session.commit()
    return jsonify({'token': login.generate_auth_token().decode('ascii'), 'error': None}), 201


@user_api.route('/api/v1/users/<int:user_id>/keys', methods=['PUT'])
@auth.login_required
def update_user_keys(user_id: int):
    user = UserModel.query.filter(UserModel.id == user_id).first()  # type:UserModel
    if user is None:
        return bad_request(Error.ILLEGAL_ARGS, 'User with id ' + str(user_id) + ' not found')

    login_model = g.login  # type: LoginModel
    user = login_model.user  # type: UserModel

    if user_id != user.id:
        return bad_request(Error.ILLEGAL_ARGS, 'No permission to update user ' + str(user_id))

    registration_id = request.json.get('registration_id') # type:int
    device_id = request.json.get('device_id') # type:int
    identity_public_key = request.json.get('identity_public_key')  # type:str
    signed_pre_key = request.json.get('signed_pre_key')  # type:str
    one_time_pre_keys = request.json.get('one_time_pre_keys')  # type:List[int]

    if any(x is None for x in 
            [registration_id, device_id, identity_public_key, one_time_pre_keys, signed_pre_key]):
        return bad_request(Error.MISSING_ARGS)

    user.registration_id = registration_id
    user.device_id = device_id
    user.identity_public_key = identity_public_key
    user.signed_pre_key = signed_pre_key
    user.one_time_pre_keys = one_time_pre_keys

    db.session.commit()
    return jsonify({'user': user.to_dict(), 'error': None}), 201


@user_api.route('/api/v1/users/<int:user_id>/keys', methods=['GET'])
@auth.login_required
def get_other_user_keys(user_id: int):
    user = UserModel.query.filter(UserModel.id == user_id).first()  # type:UserModel
    if user is None:
        return bad_request(Error.ILLEGAL_ARGS, 'User with id ' + str(user_id) + ' not found')
    user_dict = user.to_public_dict()
    user.one_time_pre_keys =  user.one_time_pre_keys[1:]
    db.session.commit()
    return jsonify({'user': user_dict, 'error': None})


@user_api.route('/api/v1/users/<int:user_id>/friends', methods=['GET'])
@auth.login_required
def get_all_friends(user_id: int):
    user = UserModel.query.filter(UserModel.id == user_id).first()  # type:UserModel
    if user is None:
        return bad_request(Error.ILLEGAL_ARGS, 'User with id ' + str(user_id) + ' not found')
    
    login_model = g.login  # type: LoginModel
    user = login_model.user  # type: UserModel
    if user_id != user.id:
        return bad_request(Error.ILLEGAL_ARGS, 'No permission to view friends of user ' + str(user_id))

    friend_list = user.friends
    friends = []

    if friend_list is None:
      return jsonify({'friends': [], 'error': None});

    for friend_user_id in friend_list:
        friend_user = UserModel.query.filter(UserModel.id == friend_user_id).first()  # type:UserModel
        friend_registration_id = friend_user.registration_id
        friend_device_id = friend_user.device_id

        friend_user_login = LoginModel.query.filter(LoginModel.user_id == friend_user_id).first()
        friend_username = friend_user_login.username
        friends.append({
            'user_id': friend_user_id, 'username': friend_username, 
            'registration_id': friend_registration_id, 'device_id': friend_device_id})

    return jsonify({'friends': friends, 'error': None})


@user_api.route('/api/v1/users/<int:user_id>/friends', methods=['POST'])
@auth.login_required
def add_friend(user_id: int):
    user = UserModel.query.filter(UserModel.id == user_id).first()  # type:UserModel
    if user is None:
        return bad_request(Error.ILLEGAL_ARGS, 'User with id ' + str(user_id) + ' not found')

    login_model = g.login  # type: LoginModel
    user = login_model.user  # type: UserModel
    if user_id != user.id:
        return bad_request(Error.ILLEGAL_ARGS, 'No permission to update user ' + str(user_id))

    friend_username = request.json.get('username')
    if friend_username is None:
        return bad_request(Error.MISSING_ARGS)
    
    if login_model.username == friend_username:
        return bad_request(Error.ILLEGAL_ARGS, 'Cannot add self as friend')

    friend_login = LoginModel.query.filter_by(username=friend_username).first()
    if friend_login is None:
        return bad_request(Error.ILLEGAL_ARGS,
            'User with username \'' + friend_username + '\' not found')

    if user.friends is not None and friend_login.user_id in user.friends:
        return bad_request(Error.ILLEGAL_ARGS, 'User \'' + friend_username + '\' is already a friend')

    if user.friends is None:
        user.friends = [friend_login.user_id]
    else:
        user.friends = user.friends + [friend_login.user_id]
    db.session.commit()
    return get_other_user_keys(friend_login.user_id), 201


@user_api.route('/api/v1/users/<int:user_id>/friends/<int:friend_user_id>', methods=['POST'])
@auth.login_required
def remove_friend(user_id: int, friend_user_id: int):
    user = UserModel.query.filter(UserModel.id == user_id).first()  # type:UserModel
    if user is None:
        return bad_request(Error.ILLEGAL_ARGS, 'User with id ' + str(user_id) + ' not found')

    login_model = g.login  # type: LoginModel
    user = login_model.user  # type: UserModel
    if user_id != user.id:
        return bad_request(Error.ILLEGAL_ARGS, 'No permission to update user ' + str(user_id))

    if user.friends is None or friend_user_id not in user.friends:
        return bad_request(Error.ILLEGAL_ARGS, 'User \'' + str(friend_user_id) + '\' is not a friend')

    user.friends = user.friends.remove(friend_user_id)
    db.session.commit()
    return jsonify({'friends': user.friends}), 201


@user_api.route('/api/v1/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    login_model = g.login  # type: LoginModel
    user = login_model.user  # type: UserModel
    user_id = user.id # type:int

    token = login_model.generate_auth_token()
    return jsonify({'token': token.decode('ascii'), 'user_id': user_id, 'error': None})


@auth.verify_password
def verify_password(username_or_token, password):
    login = LoginModel.verify_auth_token(username_or_token)
    if not login:
        login = LoginModel.query.filter_by(username=username_or_token).first()
        if not login or not login.verify_password(password):
            return False
    g.login = login  # type: LoginModel
    return True
