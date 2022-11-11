from api.service.palette import PaletteService


class Palette:
    def get_palette_color_by_photo_id(self, photo_id):
        # 分析根据主色分析三色标
        palette_color = PaletteService()
        palette_list = palette_color.parse_palette3(photo_id)
        if palette_list is not None:
            return palette_list
        else:
            return False
