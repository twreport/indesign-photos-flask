from flask import Blueprint, request, jsonify
from api.controller.roles import Roles
from api.utils.responses import response_with
from api.utils import responses as resp

roles_routes = Blueprint("roles_routes", __name__)

@roles_routes.route('/', methods=['GET'])
def get_roles_all():
    roles = Roles()
    result = roles.get_all_roles()
    return response_with(resp.SUCCESS_200, value={"result": result})