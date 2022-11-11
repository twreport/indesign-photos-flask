
from api.service.coordinate import CoordinateService
from api.utils import constants as cons


class StandardsService:
    def add_standard_id_2_color_list(self, color_list):
        for i in range(cons.NUM_CLUSTERS):
            rgb_arr = color_list[i]['rgb']
            standard_id = self.get_standard_id_by_rgb(rgb_arr)
            color_list[i]['standard_id'] = standard_id
        return color_list

    def get_standard_id_by_rgb(self, rgb_arr):
        limit = 50
        coordinate = CoordinateService()
        near_color_fetched = coordinate.get_near_colors(rgb_arr, limit, 'n130')
        standard_id = self.get_most_near_color(near_color_fetched, rgb_arr)
        return standard_id

    def get_most_near_color(self, near_color_fetched, rgb_arr):
        diff = 10000000
        r, g, b = rgb_arr
        standard_id = 0
        for color in near_color_fetched:
            # 传统算法
            # r_diff = (color.red - r) * (color.red - r)
            # g_diff = (color.green - g) * (color.green - g)
            # b_diff = (color.blue - b) * (color.blue - b)
            # all_diff = r_diff + g_diff + b_diff

            # lab2000算法
            coordinate = CoordinateService()
            color_rgb_arr = [color.red, color.green, color.blue]
            all_diff = coordinate.get_color_diff_lab(rgb_arr, color_rgb_arr)

            if all_diff < diff:
                diff = all_diff
                standard_id = color.id

        return standard_id