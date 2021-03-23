# @Description:
# 


# @Time : 2021/3/22 15:46 
# @Author : Woqi
# @File : urls.py 
# @Software: PyCharm
from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'login/$', views.login, name="login"),
    url(r'register/$', views.register, name="register"),
    url(r'article/(\d+)/$', views.article, name="article"),
    url(r'index/$', views.index, name="index"),
]
