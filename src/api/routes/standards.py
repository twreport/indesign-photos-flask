from flask import Blueprint, request, jsonify
from api.controller.standards import Standards
from api.utils.responses import response_with
from api.utils import responses as resp

standards_routes = Blueprint("standards_routes", __name__)

@standards_routes.route('/', methods=['GET'])
def get_standards_list():
    standards = Standards()
    result = standards.get_all_standard_colors()
    return response_with(resp.SUCCESS_200, value={"result": result})

@standards_routes.route('/<int:standard_id>', methods=['GET'])
def get_standard_by_id(standard_id):
    standards = Standards()
    result = standards.get_standard_color_by_id(standard_id)
    return response_with(resp.SUCCESS_200, value={"result": result})

@standards_routes.route('/coordinate/<int:r>/<int:g>/<int:b>', methods=['GET'])
def get_rgb_coordinate(r, g, b):
    standards = Standards()
    result = standards.get_rgb_coordinate(r, g, b)
    return response_with(resp.SUCCESS_200, value={"result": result})

@standards_routes.route('/coordinate/n1351/<int:r>/<int:g>/<int:b>', methods=['GET'])
def get_rgb_coordinate_by_n1351(r, g, b):
    standards = Standards()
    result = standards.get_rgb_coordinate_by_n1351(r, g, b)
    return response_with(resp.SUCCESS_200, value={"result": result})