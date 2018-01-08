from collections import defaultdict

from django.db import models
import django.utils.timezone as timezone
from django.utils.html import strip_tags

from DjangoUeditor.models import UEditorField

from utils import validators


# Create your models here.

# 标签表：标签id,标签名,标签url
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name="标签")
    Weights = models.IntegerField(default=1, verbose_name="权重", validators=validators.IntValidators())

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 分类表：分类id，分类名，分类url，分类权重
class Category(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True, verbose_name="分类")
    Weights = models.IntegerField(default=1, verbose_name="权重", validators=validators.IntValidators())
    SubClass = models.ForeignKey("self", verbose_name="父分类", null=True, blank=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name
        # 设置按权重排序，相同则按id倒序排列
        ordering = ['-Weights', '-id']

    def __str__(self):
        return self.name


# 文章表：文章id,文章标题，文章描述，文章内容，创建时间，最近修改时间
#               是否原创，是否推荐，阅读量，标签(外键，多对多) 分类(外键)
class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="标题", null=False)
    # 文章唯一性标识
    url = models.CharField(verbose_name="文章hash", max_length=100, null=True, blank=True)
    desc = models.CharField(max_length=128, verbose_name="描述", null=True, blank=True)
    # content = models.TextField(blank=True, null = True,verbose_name = "文章内容")
    Content = UEditorField(
        '文章内容', height=100, width=500,
        toolbars='full', blank=True, imagePath="upload/image/",
    )

    create_date = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    modify_date = models.DateTimeField(default=timezone.now, verbose_name="修改时间")
    tags = models.ManyToManyField(Tag, verbose_name="标签")
    category = models.ForeignKey(Category, verbose_name="分类")
    click_count = models.IntegerField(default=1, verbose_name="浏览量", validators=validators.IntValidators(min=0, max=1.1))

    is_publish = models.BooleanField(default=False, verbose_name="是否发布")
    is_recommend = models.BooleanField(default=False, verbose_name="是否推荐")

    is_original = models.BooleanField(default=True, verbose_name="是否原创")
    url_old = models.CharField("原文链接", null=True, blank=True, max_length=100)
    website = models.CharField(verbose_name="来源站点", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-create_date', ]

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.desc:
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.desc = strip_tags(self.Content)[:54]

        if not self.url:
            self.url = "%s-%s" % (self.id, self.title)[:99]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Article, self).save(*args, **kwargs)

# 友链表：id,名称 ，url,权重
class Link(models.Model):
    name = models.CharField(max_length=20, verbose_name="站点名")
    url = models.URLField(blank=True, verbose_name="链接")
    Weights = models.IntegerField(
        default=1, verbose_name="权重", validators=validators.IntValidators())
    is_publish = models.BooleanField(default=False, verbose_name="是否批准")
    desc = models.TextField(verbose_name="站点说明", blank=True, default="")

    class Meta:
        verbose_name = "友链"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
