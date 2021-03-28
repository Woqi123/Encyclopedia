from django.shortcuts import render, redirect

# Create your views here.
from app01 import models
import hashlib
from app01.forms import RegForm, ArticleForm, ArticleDetailForm
from app01.util.pagination import Pagination


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
    # is_login = request.session.get('is_login')
    # username = request.session.get('username')
    # print(is_login, username)
    return render(request, 'index.html', {"all_articles": all_article})


def article(request, pk):
    article = models.Article.objects.get(pk=pk)
    return render(request, 'article.html', {"article": article})


def register(request):
    reg_form = RegForm()
    if request.method == "POST":
        reg_form = RegForm(request.POST, request.FILES)
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
    articles_list = models.Article.objects.all()
    pagination = Pagination(request, len(articles_list), 4)
    return render(request, "article_list.html",
                  {'articles_list': articles_list[pagination.start: pagination.end], "page": pagination.page,
                   "total_page": range(pagination.page_start, pagination.page_end + 1)})


def article_add(request):
    form_obj = ArticleForm()
    article_detail_form = ArticleDetailForm()
    if request.method == 'POST':
        form_obj = ArticleForm(request.POST)
        article_detail_form = ArticleDetailForm(request.POST)

        if form_obj.is_valid() and article_detail_form.is_valid():
            detail_obj = article_detail_form.save()
            form_obj.cleaned_data['detail_id'] = detail_obj.pk
            models.Article.objects.create(**form_obj.cleaned_data)
            return redirect('article_list')

    return render(request, "article_add.html", {'form_obj': form_obj, "article_detail_form": article_detail_form})


def article_edit(request, pk):
    article_obj = models.Article.objects.filter(pk=pk).first()
    form_obj = ArticleForm(instance=article_obj)
    article_detail_form = ArticleDetailForm(instance=article_obj.detail)

    if request.method == "POST":
        form_obj = ArticleForm(request.POST, instance=article_obj)
        article_detail_form = ArticleDetailForm(request.POST, instance=article_obj.detail)

        if form_obj.is_valid() and article_detail_form.is_valid():
            # form_obj.instance.detail.content = request.POST.get('detail')
            # form_obj.instance.detail.save()
            article_detail_form.save()
            form_obj.save()
            return redirect('article_list')
    return render(request, 'article_edit.html',
                  {'article_obj': article_obj, 'form_obj': form_obj, 'article_detail_form': article_detail_form})


def user_list(request):
    user_list = [{"username": "woqi-{}".format(i), "password": "123456"} for i in range(309)]
    pagination = Pagination(request, len(user_list))
    return render(request, "user_list.html",
                  {"user_list": user_list[pagination.start: pagination.end], "page": pagination.page,
                   "total_page": range(pagination.page_start, pagination.page_end + 1)})
