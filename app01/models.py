from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='用户密码', max_length=32)
    position = models.CharField(verbose_name='职位', max_length=32)
    company = models.CharField(verbose_name="公司",
                               choices=(("", "公司选择"), ('1', '深圳总公司'), ('2', '武汉分公司'), ('3', '北京分公司')),
                               max_length=32)
    phone = models.CharField(verbose_name="联系方式", max_length=11)
    creat_time = models.DateTimeField(verbose_name="注册时间", auto_now_add=True)
    last_time = models.DateTimeField(verbose_name="最后一次登录时间", auto_now=True, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="是否激活", default=True)
    profile = models.ImageField(verbose_name="头像", upload_to="image/profile", default="image/profile/default.jpg")

    def __str__(self):
        return self.username


class Category(models.Model):
    title = models.CharField(verbose_name="板块标题", max_length=64)

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    标题，文章摘要，文章内容(另外一张表存放)，作者，板块，创建时间，更新时间，删除状态
    """
    PUBSTATUS = ((False, "未发布"), (True, "已发布"))

    title = models.CharField(verbose_name="标题", max_length=64, unique=True)
    abstract = models.CharField(verbose_name="文章摘要", max_length=256)
    author = models.ForeignKey(User, to_field="username", verbose_name="作者", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, verbose_name="分类板块", on_delete=models.SET_NULL, null=True)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    delete_status = models.BooleanField(verbose_name="是否删除", default=False)
    publish_status = models.BooleanField(verbose_name="发布状态", choices=PUBSTATUS, default=False)
    detail = models.OneToOneField("ArtileDetail", verbose_name="文章详情", on_delete=models.SET_NULL, null=True)


from ckeditor_uploader.fields import RichTextUploadingField


class ArtileDetail(models.Model):
    content = RichTextUploadingField(verbose_name="文章内容")


class Comment(models.Model):
    """
    评论表： 评论者、评论内容、审核状态、评论时间，关联文章
    """
    user = models.ForeignKey("User", verbose_name="评论者", on_delete=models.SET_NULL, null=True)
    content = models.TextField(verbose_name="评论内容")
    article = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True)
    audit_status = models.BooleanField(verbose_name="审核状态", default=True)
    time = models.DateTimeField(verbose_name="评论时间", auto_now_add=True)
