from flask import Blueprint, request, jsonify
from api.controller.photos import Photos
from api.utils.responses import response_with
from api.utils import responses as resp

photos_routes = Blueprint("photos_routes", __name__)

@photos_routes.route('/', methods=['GET'])
def get_photos_all():
    photos = Photos()
    result = photos.get_all_photos()
    return response_with(resp.SUCCESS_200, value={"result": result})

@photos_routes.route('/status/', methods=['GET'])
def get_one_photo_by_status():
    photos = Photos()
    result = photos.get_one_photo_by_status()
    return response_with(resp.SUCCESS_200, value={"result": result})

@photos_routes.route('/status/<int:photo_id>', methods=['GET'])
def get_main_color_by_photo_id(photo_id):
    photos = Photos()
    result = photos.get_main_color_by_photo_id(photo_id)
    return response_with(resp.SUCCESS_200, value={"result": result})

@photos_routes.route('/color_list/<int:photo_id>', methods=['GET'])
def parse_special_color(photo_id):
    photos = Photos()
    result = photos.parse_special_color(photo_id)
    return response_with(resp.SUCCESS_200, value={"result": result})

@photos_routes.route('/merge_color/<int:photo_id>', methods=['GET'])
def merge_color(photo_id):
    photos = Photos()
    result = photos.merge_color(photo_id)
    return response_with(resp.SUCCESS_200, value={"result": result})

