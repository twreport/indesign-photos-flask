# 图片路径
BASE_URL = '/indesign/www/html/tp5/public/static/uploads/'
# 分析图片主色的数量，默认：5
NUM_CLUSTERS = 5
# 分析主题色的数量
NUM_CLUSTERS_SPECIAL = 20
# 主色数量
NUM_MAIN_COLORS = 5
# 特殊色数量
NUM_SPECIAL_COLORS = 2
# 最接近颜色色差的阀值
CLOSE_COLOR_LIMIT_RGB = 100
# 最接近颜色色差的hls中h的阀值
CLOSE_COLOR_LIMIT_H = 3

# 主题色饱和度阀值
SPECIAL_COLOR_LIMIT_S = 0.1

SPECIAL_COLOR_LIMIT_H_TOP = 0.9

SPECIAL_COLOR_LIMIT_H_BOTTOM = 0.1

# 低色值颜色列表
LOW_COLOR_STANDARD_LIST = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 111,
                           112, 113, 114, 115, 116, 117, 118, 119, 120,
                           121, 122, 123, 124, 125, 126, 127, 128, 129, 130]

