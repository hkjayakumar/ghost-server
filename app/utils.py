import datetime
from typing import List
from flask import jsonify
from enum import Enum

def date_from_str(date_str: str) -> datetime.date:
    arr = date_str.split('/')  # type:List[str]
    return datetime.date(int(arr[0]), int(arr[1]), int(arr[2]))


def date_time_from_str(date_str: str) -> datetime.datetime:
    arr = date_str.split(' ')
    date_arr = arr[0].split('/')
    time_arr = arr[1].split(':')
    return datetime.datetime(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]), int(time_arr[0]),
                                          int(time_arr[1]), int(time_arr[2]))


def str_from_date(date: datetime.date) -> str:
    if date is None:
        return None
    return date.strftime('%Y/%m/%d')


def str_from_date_time(date: datetime.datetime) -> str:
    if date is None:
        return None
    return date.strftime('%Y/%m/%d %H:%M:%S')


#########
#  Helper Responses
#########
class Error(Enum):
    MISSING_ARGS = 1
    ILLEGAL_ARGS = 2


error_messages = {Error.MISSING_ARGS: 'Missing arguments', Error.ILLEGAL_ARGS: 'Illegal arguments'}


def bad_request(err: Error, message: str = None):
    if message is None:
        message = error_messages[err]
    err_obj = {'id': err.value, 'message': message}
    response = jsonify({'error': err_obj})
    response.status_code = 400
    return response
