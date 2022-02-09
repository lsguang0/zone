from flask import request, jsonify
from utils import check_user_list, check_user_register


def login_check(data):
    username = data.get("username")
    password = data.get("password")

    if not all([username, password]):
        return jsonify({'status': 400, 'msg': '信息不完整'})
    return check_user_list(username, password)


def register_check(data):
    username = data.get("username")
    password = data.get("password")

    return check_user_register(username, password)
