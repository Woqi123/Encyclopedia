from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

# Create your views here.
from app01 import models


def login(request):
    if request.method == "POST":
        username = request.POST.get("user", "")
        password = request.POST.get("pwd", "")
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        user_obj = models.User.objects.filter(username=username, password=md5.hexdigest(), is_active=True)
        if user_obj:
            # 登录成功，保存登录状态 用户名
            request.session['is_login'] = True
            request.session['username'] = username
            url = request.GET.get('url', "")
            return redirect(url) if url else redirect('index')
        error = "用户名或密码错误"
    return render(request, 'login.html', locals())


def index(request):
    # 查询所有文章
    all_article = models.Article.objects.all()
    is_login = request.session.get('is_login')
    username = request.session.get('username')
    print(is_login, username)
    return render(request, 'index.html', {"all_articles": all_article})


def article(request, pk):
    article = models.Article.objects.get(pk=pk)
    return render(request, 'article.html', {"article": article})


from django import forms
import hashlib


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


def register(request):
    reg_form = RegForm()
    if request.method == "POST":
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            # 注册成功，跳转到登录页面
            print(request.POST)
            print(reg_form.cleaned_data)
            reg_form.cleaned_data.pop('re_pwd')
            models.User.objects.create(**reg_form.cleaned_data)
            return redirect("login")
    return render(request, "register.html", {'reg_form': reg_form})


def backend(request):
    return render(request, "dashboard.html")


def logout(request):
    request.session.flush()
    url = request.GET.get('url', "")
    return redirect(url) if url else redirect('index')


def article_list(request):
    all_articles = models.Article.objects.all()
    return render(request, "request_list.html", {'aall_article': all_articles})
