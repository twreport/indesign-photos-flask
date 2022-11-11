from flask import Blueprint, request, jsonify
from api.controller.users import Users
from api.utils.responses import response_with
from api.utils import responses as resp

users_routes = Blueprint("users_routes", __name__)

@users_routes.route('/', methods=['GET'])
def get_users_list():
    users = Users()
    result = users.get_all_users()
    return response_with(resp.SUCCESS_200, value={"result": result})

@users_routes.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    users = Users()
    result = users.get_user_by_id(user_id)
    return response_with(resp.SUCCESS_200, value={"result": result})

@users_routes.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    users = Users()
    result = users.add_user(data)
    return response_with(resp.SUCCESS_200, value={"result": result})

@users_routes.route('/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    users = Users()
    result = users.delete_user_by_id(user_id)
    return response_with(resp.SUCCESS_200, value={"result": result})

@users_routes.route('/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    data = request.get_json()
    users = Users()
    result = users.update_user_by_id(user_id, data)
    return response_with(resp.SUCCESS_200, value={"result": result})

@users_routes.route('/user_role/<int:user_id>', methods=['GET'])
def get_user_with_role_by_id(user_id):
    users = Users()
    result = users.get_user_with_role_by_id(user_id)
    return response_with(resp.SUCCESS_200, value={"result": result})


