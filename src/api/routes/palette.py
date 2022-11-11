from flask import Blueprint, request, jsonify
from api.controller.palette import Palette
from api.utils.responses import response_with
from api.utils import responses as resp

palette_routes = Blueprint("palette_routes", __name__)

@palette_routes.route('/photo/<int:photo_id>', methods=['GET'])
def get_palette_color_by_photo_id(photo_id):
    print('route palette!')
    palette = Palette()
    result = palette.get_palette_color_by_photo_id(photo_id)
    return response_with(resp.SUCCESS_200, value={"result": result})

