import math
from sqlalchemy import or_, and_
from api.model.standards import ColorStandard
from api.model.standards_n1351 import ColorStandardN1351


class CoordinateService:
    def get_rgb_coordinate_by_n1351(self, input_color):
        limit = 10
        step = 2
        first_selected_color = 8
        while limit < 255:
            near_colors = self.get_near_colors(input_color, limit, 'n1351')
            if len(near_colors) >= first_selected_color:
                break
            limit = limit + step

        # 2-从这些颜色里筛选出色差最小的3个颜色
        diff_dict_all = self.order_nearest_3(input_color, near_colors)

        # 使用三点定位法计算输入颜色的色彩形象坐标
        coordinate = self.calculate_coordinate(diff_dict_all)
        return coordinate
    
    def get_rgb_coordinate(self, input_color):
        # 1-根据不同限定获得距离最近的n个颜色
        limit = 50
        step = 10
        first_selected_color = 5
        while limit < 255:
            near_colors = self.get_near_colors(input_color, limit)
            if len(near_colors) >= first_selected_color:
                break
            limit = limit + step

        # 2-从这些颜色里筛选出色差最小的3个颜色
        diff_dict_all = self.order_nearest_3(input_color, near_colors)

        # 使用三点定位法计算输入颜色的色彩形象坐标
        coordinate = self.calculate_coordinate(diff_dict_all)
        return coordinate

    def calculate_coordinate(self, diff_dict_all):
        coordinates = []
        for diff_dict in diff_dict_all:
            diff = diff_dict_all[diff_dict]
            coordinates.append(diff)

        coordinate0, coordinate1, coordinate2 = coordinates

        # 先按照两点之间色差比例，计算出色差最近点的坐标
        coordinate0_1 = self.get_coordinate_between_2(coordinate0, coordinate1)
        coordinate0_1_2 = self.get_coordinate_between_2(coordinate0_1, coordinate2)

        return coordinate0_1_2

    def get_coordinate_between_2(self, coordinate0, coordinate1):
        # 计算出三角形的两个直角边长
        diff_x = coordinate0['x'] - coordinate1['x']
        diff_y = coordinate0['y'] - coordinate1['y']

        # 计算出色差比例
        ratio = coordinate0['diff'] / (coordinate0['diff'] + coordinate1['diff'])

        # 按色差比例分配坐标
        x = coordinate0['x'] - (diff_x * ratio)
        y = coordinate0['y'] - (diff_y * ratio)

        # 装配返回数据
        coordinate_dict = {}
        coordinate_dict['id'] = 0
        coordinate_dict['x'] = round(x)
        coordinate_dict['y'] = round(y)
        # 新数据的色差按最小色差计算
        coordinate_dict['diff'] = coordinate0['diff']
        return coordinate_dict

    def get_near_colors(self, input_color, limit, db='n130'):
        r, g, b =input_color
        r_limit = self.get_limit(r, limit)
        g_limit = self.get_limit(g, limit)
        b_limit = self.get_limit(b, limit)
        
        if db == 'n130':
            color_filter = {
                and_(
                    ColorStandard.red >= r_limit[0],
                    ColorStandard.red <= r_limit[1],
                    ColorStandard.green >= g_limit[0],
                    ColorStandard.green <= g_limit[1],
                    ColorStandard.blue >= b_limit[0],
                    ColorStandard.blue <= b_limit[1]
                )
            }
            fetched = ColorStandard.query.filter(*color_filter).all()
        elif db == 'n1351':
            color_filter = {
                and_(
                    ColorStandardN1351.red >= r_limit[0],
                    ColorStandardN1351.red <= r_limit[1],
                    ColorStandardN1351.green >= g_limit[0],
                    ColorStandardN1351.green <= g_limit[1],
                    ColorStandardN1351.blue >= b_limit[0],
                    ColorStandardN1351.blue <= b_limit[1]
                )
            }
            fetched = ColorStandardN1351.query.filter(*color_filter).all()
        else:
            fetched = None

        return fetched

    def order_nearest_3(self, input_color, near_colors):
        diff_dict_all = {}
        for color in near_colors:
            diff_dict = {}

            color_list = [color.red, color.green, color.blue]
            # diff = self.get_color_diff(input_color, color_list)
            diff = self.get_color_diff_lab(input_color, color_list)
            diff_dict['id'] = color.id
            diff_dict['x'] = color.x
            diff_dict['y'] = color.y
            diff_dict['diff'] = diff
            diff_dict_all[diff] = diff_dict

        sort = sorted(diff_dict_all.keys())

        i = 0
        final_diff = {}
        for diff_key in sort:

            final_diff[diff_key] = diff_dict_all[diff_key]
            i = i + 1
            if i >= 3:
                break

        return final_diff

    def get_color_diff(self, c1, c2):
        diff_r = c1[0] - c2[0]
        diff_g = c1[1] - c2[1]
        diff_b = c1[2] - c2[2]
        diff = round(math.sqrt(diff_r * diff_r + diff_g * diff_g + diff_b * diff_b))
        return diff

    def get_color_diff_lab(self, rgb_1, rgb_2):
        R_1, G_1, B_1 = rgb_1
        R_2, G_2, B_2 = rgb_2
        rmean = (R_1 + R_2) / 2
        R = R_1 - R_2
        G = G_1 - G_2
        B = B_1 - B_2
        return round(math.sqrt((2 + rmean / 256) * (R ** 2) + 4 * (G ** 2) + (2 + (255 - rmean) / 256) * (B ** 2)))

    # 获得给定rgb值的上下限
    def get_limit(self, color, limit):
        _i = color - limit
        if _i < 0:
            _i = 0

        i_ = color + limit
        if i_ > 255:
            i_ = 255

        return _i, i_
