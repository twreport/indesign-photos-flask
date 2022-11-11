from api.model.photos import ColorPhotos
from api.model.photos import ColorPhotosSchema
from api.service.photos import PhotoColorService as PhotoColor
from api.service.standards import StandardsService

class Photos:
    def get_all_photos(self):
        fetched = ColorPhotos.query.all()
        photos_schema = ColorPhotosSchema(many=True)
        photos = photos_schema.dump(fetched)
        return photos

    def get_one_photo_by_status(self):
        # 任意找出一个刚刚上传的图片
        fetched = ColorPhotos.query.filter_by(status=0).first()

        photo_color = PhotoColor()
        color_list = photo_color.parse(fetched.sm_url)

        # 得到与5种主色最接近的标准色，进一步完善主色dict
        standards = StandardsService()
        color_list_with_standard_id = standards.add_standard_id_2_color_list(color_list)
        return color_list_with_standard_id

        # result = self.update_color_info_in_db(fetched, color_dict)
        # return result
    
    def get_main_color_by_photo_id(self, photo_id):
        # 获取数据库中的图片
        fetched = ColorPhotos.query.get(photo_id)

        # 分析出n种主色
        photo_color = PhotoColor()
        color_list = photo_color.parse(fetched.sm_url)

        # 得到与n种主色最接近的标准色，进一步完善主色dict
        standards = StandardsService()
        color_list_with_standard_id = standards.add_standard_id_2_color_list(color_list)
        if color_list_with_standard_id:
            return color_list_with_standard_id
        else:
            return False

    def update_color_info_in_db(self, fetched, color_list):
        # rgb0 = ','.join(color_list[0].rgb)
        # rgb1 = ','.join(color_list[1].rgb)
        # rgb2 = ','.join(color_list[2].rgb)
        # rgb3 = ','.join(color_list[3].rgb)
        # rgb4 = ','.join(color_list[4].rgb)
        # fetched.color_1_rgb = rgb0
        # fetched.color_1_weight = color_list[0].weight
        # fetched.
        return True

    def parse_special_color(self, photo_id):

        # 获取数据库中的图片
        fetched = ColorPhotos.query.get(photo_id)

        photo_color = PhotoColor()
        result = photo_color.parse_special_color(fetched.sm_url)
        return result

    def merge_color(self, photo_id):

        # 获取数据库中的图片
        fetched = ColorPhotos.query.get(photo_id)

        photo_color = PhotoColor()
        result = photo_color.merge_color(fetched.sm_url)
        return result


