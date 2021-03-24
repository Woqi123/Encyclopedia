# @Description:
# 


# @Time : 2021/3/24 16:42 
# @Author : Woqi
# @File : my_middleware.py 
# @Software: PyCharm
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
import re


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 需要登录后访问的地址，判断登录状态
        # 默认所有地址都需要登录状态才能访问
        # 设置登陆白名单 不登录则不能访问
        url = request.path_info
        # 正则匹配访问白名单
        for white_url in settings.WHITE_LIST:
            if re.match(white_url, url):
                return
        is_login = request.session.get('is_login')
        # 状态为已登录
        if is_login:
            return
        # 跳转登录页面
        return redirect("{}?url={}".format(reverse('login'), url))
