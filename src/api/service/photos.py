import numpy as np
import cv2 as cv
import colorsys
from api.service.coordinate import CoordinateService
from api.service.standards import StandardsService
from api.utils import constants as cons
from operator import itemgetter


class PhotoColorService:
    public_color_list = []

    # 用kmeans模块分析图像颜色
    # image - opencv读取的图片
    # num_clusters - 多少个中心点
    def parse_photo_by_k_means(self, image, num_clusters):
        h, w, ch = image.shape
        data = image.reshape((-1, 3))
        data = np.float32(data)

        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv.kmeans(data, num_clusters, None, criteria, num_clusters, cv.KMEANS_RANDOM_CENTERS)
        clusters = np.zeros(num_clusters, dtype=np.int32)
        for i in range(len(label)):
            clusters[label[i]] += 1

        clusters = np.float32(clusters) / float(h * w)
        center = np.int32(center)

        # 将open-cv的bgr换成rgb
        rgb_center = self.bgr2rgb(center, num_clusters)
        photo_color_list = self.format_color_list(clusters, rgb_center)

        # 返回color列表
        return photo_color_list

    def format_color_list(self, clusters, rgb_center):

        # 1-按颜色占比逆序排序
        k_means_matrix = []
        # 组合成二维列表以便排序
        for i in range(len(clusters)):
            k_means_matrix_item = []
            # 占比单位万分之一
            k_means_matrix_item.append(int(clusters[i] * 10000))
            k_means_matrix_item.append(rgb_center[i])
            k_means_matrix.append(k_means_matrix_item)
        k_means_matrix = sorted(k_means_matrix, key=itemgetter(0), reverse=True)

        # 2-组合成字典列表
        photo_color_dict_sorted = []
        for i in range(len(k_means_matrix)):
            color_dict = {}
            color_dict['rgb'] = k_means_matrix[i][1]
            color_dict['weight'] = k_means_matrix[i][0]
            photo_color_dict_sorted.append(color_dict)
        return photo_color_dict_sorted

    def parse(self, url):
        num_clusters = cons.NUM_CLUSTERS
        full_url = cons.BASE_URL + url
        image = cv.imread(full_url)

        # 用kmeans分析照片主要颜色
        photo_color_list = self.parse_photo_by_k_means(image, num_clusters)
        photo_main_color_list = self.add_standard_id_to_list(photo_color_list)

        print("----------------------------main_color_with_standard_id-------------------------")
        for i in photo_main_color_list:
            print(i)

        return photo_main_color_list

    def add_standard_id_to_list(self, photo_color_list):
        # 分析标准色id
        ss = StandardsService()
        final_color_list = []
        for color in photo_color_list:
            color['standard_id'] = ss.get_standard_id_by_rgb(color['rgb'])
            final_color_list.append(color)

        return final_color_list

    def bgr_arr_2_rgb_str_arr(self, bgr_arr):
        rgb_str_arr = []
        rgb_arr = self.bgr2rgb(bgr_arr)
        for i in range(cons.NUM_CLUSTERS):
            rgb_str = str(rgb_arr[i][0]) + ',' + str(rgb_arr[i][1]) + ',' + str(rgb_arr[i][2])
            rgb_str_arr.append(rgb_str)
        return rgb_str_arr

    def bgr2rgb(self, bgr_arr, num_clusters):
        rgb_arr = []
        for c in range(num_clusters):
            b = bgr_arr[c][0]
            g = bgr_arr[c][1]
            r = bgr_arr[c][2]
            rgb_arr_item = [int(r), int(g), int(b)]
            rgb_arr.append(rgb_arr_item)
        return rgb_arr

    def parse_special_color(self, url):
        num_clusters = cons.NUM_CLUSTERS_SPECIAL
        full_url = cons.BASE_URL + url
        image = cv.imread(full_url)

        # 用kmeans分析照片主要颜色
        photo_color_list = self.parse_photo_by_k_means(image, num_clusters)

        # 添加hls信息
        color_list_with_hls = self.add_hls_to_color_list(photo_color_list)
        # 添加标准色信息
        special_color_with_hls = self.add_standard_id_to_list(color_list_with_hls)
        # 用hls信息筛选饱和度高、色彩鲜明的主题色
        special_color_with_hls = self.select_special_color_by_hls(special_color_with_hls)


        print("----------------------------special_color_with_hls-------------------------")
        for i in special_color_with_hls:
            print(i)
        return special_color_with_hls

    def add_hls_to_color_list(self, color_list):
        color_list_with_hls = []
        for color in color_list:
            color['hls'] = self.rgb2hls(color['rgb'])
            color_list_with_hls.append(color)
        return color_list_with_hls

    # hls体系：h-360度色环，lightness和Saturation均大于0小于1
    def rgb2hls(self, rgb_list):
        r, g, b = rgb_list
        r = r / 255.0
        g = g / 255.0
        b = b / 255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return h * 360, l, s

    # def select_special_color_by_hls(self, special_color_with_hls):
    #     result = [{}, {}, {}]
    #     s1 = 0
    #     s2 = 0
    #     s3 = 0
    #     for s_color in special_color_with_hls:
    #         h, l, s = s_color['hls']
    #         if s > s1 and l < 0.9 and l > 0.15 and s > 0.1:
    #             s1 = s
    #             result[0] = s_color
    #         elif s > s2 and s != s1 and l < 0.9 and l > 0.15 and s > 0.1:
    #             s2 = s
    #             result[1] = s_color
    #         elif s > s3 and s != s1 and s != s2 and l < 0.9 and l > 0.15 and s > 0.1:
    #             s3 = s
    #             result[2] = s_color
    #         else:
    #             pass
    #     return result

    def select_special_color_by_hls(self, special_color_with_hls):
        # 1-按饱和度占比逆序排序
        s_color_matrix = []
        # 组合成二维列表以便排序
        for color in special_color_with_hls:
            s_color_matrix_item = []
            h, l, color_s = color['hls']
            s_color_matrix_item.append(color_s)
            s_color_matrix_item.append(color)
            s_color_matrix.append(s_color_matrix_item)
        # 排序
        s_color_matrix = sorted(s_color_matrix, key=itemgetter(0), reverse=True)

        # 还原颜色列表
        result = []
        standard_list = []
        print(s_color_matrix)
        for s_color in s_color_matrix:
            h, l, s = s_color[1]['hls']
            standard_id = s_color[1]['standard_id']
            if s > cons.SPECIAL_COLOR_LIMIT_S and cons.SPECIAL_COLOR_LIMIT_H_TOP \
                    and l > cons.SPECIAL_COLOR_LIMIT_H_BOTTOM and len(result) < 3\
                    and standard_id not in standard_list\
                    and standard_id not in cons.LOW_COLOR_STANDARD_LIST:
                standard_list.append(standard_id)
                result.append(s_color[1])

        return result



    def group_special_color(self, special_color_list):
        print("----------------------------special_color_list-------------------------")
        for i in special_color_list:
            print(i)

        # 将h抽取出来作为颜色标记
        h_list = []
        for color in special_color_list:
            h, l, s = color['hls']
            color['h'] = h
            h_list.append(color)

        # 分组相近颜色
        group_color_list = []
        already_grouped_list = []
        for base_color in h_list:
            group_color_list_item = []
            # 如果比较色没有被别的颜色分组
            if base_color not in already_grouped_list:
                group_color_list_item.append(base_color)
                for compare_color in h_list:
                    # 实例化坐标服务，调用坐标服务里的色差计算器
                    cs = CoordinateService()
                    diff_rgb = cs.get_color_diff_lab(base_color['rgb'], compare_color['rgb'])
                    diff_h = abs(base_color['h'] - compare_color['h'])
                    # 如果色差小于阀值，且被比较色不是比较色，且被比较色没有被合并
                    if diff_h < cons.CLOSE_COLOR_LIMIT_H and base_color != compare_color \
                            and diff_rgb < cons.CLOSE_COLOR_LIMIT_RGB and compare_color not in already_grouped_list:
                        group_color_list_item.append(compare_color)
                        already_grouped_list.append(compare_color)
                    else:
                        pass
                group_color_list.append(group_color_list_item)
        print("----------------------------group_color_list-------------------------")
        for j in group_color_list:
            print(j)

        # 合并相近颜色
        merged_special_color_list = []
        for merged_color in group_color_list:
            merged_special_color_list_item = merged_color[0]
            if len(merged_color) > 1:
                weight_total = 0
                for c in merged_color:
                    weight_total = weight_total + c['weight']
                merged_special_color_list_item['weight'] = weight_total

            merged_special_color_list.append(merged_special_color_list_item)

        print("----------------------------merged_special_color_list-------------------------")
        for k in merged_special_color_list:
            print(k)

        return merged_special_color_list


    # 合并相近色函数
    # 最大的逻辑就是只要跟比例大的色块非常接近，就取最大色块的值，weight=色块1+色块2

    def merge_color(self, url):

        num_clusters = cons.NUM_CLUSTERS_SPECIAL
        full_url = cons.BASE_URL + url
        image = cv.imread(full_url)

        # 用kmeans分析照片主要颜色
        photo_color_list = self.parse_photo_by_k_means(image, num_clusters)
        # 在主色列表中添加hls信息
        color_list_with_hls = self.add_hls_to_color_list(photo_color_list)
        print("----------------------------merged_special_color_list-------------------------")
        for i in color_list_with_hls:
            print(i)
        # 将相近色合并
        # merged_color_list = self.group_special_color(color_list_with_hls)

        return color_list_with_hls

    # 递归函数
    # 每循环一次就按新的list处理
    def add_close_color_to_bigger(self, color_list_with_hls):

        if len(color_list_with_hls) >= 2:
            # 实例化坐标服务，调用坐标服务里的色差计算器
            cs = CoordinateService()
    
            # 每调用一次本函数，都将第一个color与后面的color比较
            first_color = color_list_with_hls[0]
    
            # 如果color_list只剩下两个，则比较这两个color是否接近
            if len(color_list_with_hls) > 2:
                # 先将第一个color砍下来
                del color_list_with_hls[0]
                is_close = False
                for i in range(0, len(color_list_with_hls)):
                    diff = cs.get_color_diff_lab(first_color['rgb'], color_list_with_hls[i]['rgb'])
                    # 如果这个color与后面的color非常接近，则直接并入后面的color
                    if diff < cons.CLOSE_COLOR_LIMIT_RGB:
                        color_list_with_hls[i]['weight'] = color_list_with_hls[i]['weight'] + first_color['weight']
                        is_close = True
                        break

                if is_close == False:
                    # 如果这个color跟任何一个color都不接近，则存入类变量
                    self.public_color_list.append(first_color)

                # 继续调用递归函数
                self.add_close_color_to_bigger(color_list_with_hls)

            else:
                last_diff = cs.get_color_diff_lab(first_color['rgb'], color_list_with_hls[1]['rgb'])
                # 如果这两个color非常接近，则合并，否则按原顺序排列
                if last_diff < cons.CLOSE_COLOR_LIMIT_RGB:
                    first_color['weight'] = color_list_with_hls[1]['weight'] + first_color['weight']
                    self.public_color_list.append(first_color)
                else:
                    self.public_color_list.append(first_color)
                    self.public_color_list.append(color_list_with_hls[1])

        else:
            return None



