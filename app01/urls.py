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
    url(r'logout/$', views.logout, name="logout"),
    url(r'register/$', views.register, name="register"),
    url(r'article/(\d+)/$', views.article, name="article"),
    url(r'index/$', views.index, name="index"),
    url(r'backend/$', views.backend, name="backend"),
    url(r'article_list/$', views.article_list, name="article_list"),
    url(r'article_add/$', views.article_add, name="article_add"),
    url(r'article_edit/(\d+)$', views.article_edit, name="article_edit"),

    url(r'user_list/$', views.user_list, name="user_list"),

]
