# @Description:
# 


# @Time : 2021/3/27 17:23 
# @Author : Woqi
# @File : pagination.py 
# @Software: PyCharm
import math


class Pagination:
    """
    page_num:每页显示条目数
    page_show: 每一组显示的页码数
    """

    def __init__(self, request, data_length, page_num=10, page_show=11):
        try:
            self.page = int(request.GET.get('page', 1))
            if self.page <= 0:
                self.page = 1
        except Exception:
            self.page = 1

        total_page = math.ceil(data_length / page_num)
        self.start = (self.page - 1) * page_num
        self.end = self.page * page_num

        page_start = self.page - 5
        page_end = page_show if page_start <= 0 else self.page + 5
        self.page_end = total_page if page_end > total_page else page_end
        self.page_start = page_start if page_start > 0 else 1
