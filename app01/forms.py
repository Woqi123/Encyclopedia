# @Description:
# 


# @Time : 2021/3/25 14:36 
# @Author : Woqi
# @File : forms.py 
# @Software: PyCharm

from django import forms
import hashlib
from app01 import models
from django.core.exceptions import ValidationError


class RegForm(forms.ModelForm):
    # username = forms.CharField()
    password = forms.CharField(label='密码', widget=forms.PasswordInput, min_length=6)
    re_pwd = forms.CharField(label='确认密码', widget=forms.PasswordInput, min_length=6)

    class Meta:
        model = models.User
        fields = '__all__'  # ['username','password'，]
        exclude = ['last_time']
        widgets = {
            'password': forms.PasswordInput
        }
        error_messages = {
            'username': {
                'required': "必填项",
            },
            'password': {
                'required': "必填项",
            },
        }

    def clean_phone(self):
        import re
        phone = self.cleaned_data.get('phone')
        if re.match(r'^1[3-9]\d{9}', phone):
            return phone
        raise ValidationError("手机号格式不正确")

    def clean(self):
        self._validate_unique = True  # 数据库检验唯一性
        pwd = self.cleaned_data.get('password', "")
        re_pwd = self.cleaned_data.get('re_pwd', "")
        if pwd == re_pwd:
            # 对密码明文进行加密
            md5 = hashlib.md5()
            md5.update(pwd.encode('utf-8'))
            print(md5.hexdigest())
            self.cleaned_data['password'] = md5.hexdigest()
            return self.cleaned_data
        self.add_error('re_pwd', '两次密码不一致')
        raise ValidationError("两次密码不一致")


class ArticleForm(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = "__all__"
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'publish_status': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'detail': forms.Select(attrs={'class': 'form-control'}),
        }
        exclude = ['detail']
