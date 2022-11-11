from api.model.photos import ColorPhotos
from api.model.photos import ColorPhotosSchema
from api.model.palette3_n3600 import ColorPalette3N3600
from api.model.standards import ColorStandard
from api.model.standards import ColorStandardSchema
from api.model.standards_n1351 import ColorStandardN1351
from api.utils.pymysql import mysqlDB
import json

class PaletteService:
    def parse_palette3(self, photo_id):
        # 获取数据库中的图片
        fetched = ColorPhotos.query.get(photo_id)

        standard_id_list = []
        weight_list = []
        for tag in fetched.tags:
            mydb = mysqlDB()
            if tag.table_name == 'color_rgb':
                tag_data = mydb.read_db_with_table_name_and_row_id(tag.table_name, tag.row_id)
                standard_id = tag_data['standard_id'][0]
                weight = tag.weight
                standard_id_list.append(standard_id)
                weight_list.append(weight)

        print('standard_id_list', standard_id_list)
        print('weight_list', weight_list)
        standard_dict = dict(zip(standard_id_list, weight_list))

        palette_list = self.match_parse_palette3_with_standard5(standard_id_list)
        palette_results = []
        if palette_list:
            for palette in palette_list:
                print(palette)
                standard1 = ColorStandard.query.get_or_404(palette.c1)
                standard2 = ColorStandard.query.get_or_404(palette.c2)
                standard3 = ColorStandard.query.get_or_404(palette.c3)
                standard_schema = ColorStandardSchema()
                standard1_json = standard_schema.dump(standard1)
                standard2_json = standard_schema.dump(standard2)
                standard3_json = standard_schema.dump(standard3)
                palette_dict = {
                    "photo_id": photo_id,
                    "palette_id": palette.id,
                    "palette_standard_list": [{
                        "standard_id": palette.c1,
                        "standard_data": standard1_json
                    },{
                        "standard_id": palette.c2,
                        "standard_data": standard2_json
                    },{
                        "standard_id": palette.c3,
                        "standard_data": standard3_json
                    }],
                    "palette_weight": self.weight_palette_with_dict(standard_dict, standard_id_list)
                }
                print(palette_dict)
                palette_results.append(palette_dict)
            return palette_results
        else:
            return None


    def match_parse_palette3_with_standard5(self, standard_id_list):
        match = []
        for c1 in standard_id_list:
            for c2 in standard_id_list:
                for c3 in standard_id_list:
                    match1 = ColorPalette3N3600.query.filter_by(c1=c1).filter_by(
                        c2=c2).filter_by(c3=c3).first()
                    if match1:
                        match.append(match1)
        if match:
            if len(match) > 0:
                return match
        else:
            return False

    def weight_palette_with_dict(self, palette_dict, palette_list):
        print(palette_dict)
        print(palette_list)
        total = 0
        for palette in palette_list:
            total = total + palette_dict[palette]
        result = round(total / len(palette_list))
        return result

