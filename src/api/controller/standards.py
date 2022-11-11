from api.model.standards import ColorStandard
from api.model.standards import ColorStandardSchema
from api.model.standards_n1351 import ColorStandardN1351
from api.model.standards_n1351 import ColorStandardN1351Schema
from api.service.coordinate import CoordinateService as Coordinate


import math

class Standards:
    def get_all_standard_colors(self):
        fetched = ColorStandard.query.all()
        standards_schema = ColorStandardSchema(many=True)
        standards = standards_schema.dump(fetched)
        return standards


    def get_standard_color_by_id(self, standrad_id):
        fetched = ColorStandard.query.get_or_404(standrad_id)
        standard_schema = ColorStandardSchema()
        standard = standard_schema.dump(fetched)
        return standard

    def get_rgb_coordinate(self, r, g, b):
        input_color = [r, g, b]
        coordinate = Coordinate()
        rgb_coordinate = coordinate.get_rgb_coordinate(input_color)
        return rgb_coordinate

    def get_rgb_coordinate_by_n1351(self, r, g, b):
        input_color = [r, g, b]
        coordinate = Coordinate()
        rgb_coordinate = coordinate.get_rgb_coordinate_by_n1351(input_color)
        return rgb_coordinate