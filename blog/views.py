import logging

from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.db.models.aggregates import Count

from blog.models import Tag, Category, Article, Link
from blog.forms import LinkForm

logger = logging.getLogger('blog.views')


# 获取setting文件中的全局配置文件 (要设置全局解释器：settings的TEMPLATES的OPTIONS)
def global_setting(request):
    # 获取分类信息
    # category_list = Category.objects.all()
    category_list = Category.objects.annotate(num_posts=Count('article'))

    # 获取文章归档，使用的是自定义的方法
    # 抛弃自定义管理器方式 ，采用api提供了dates排序切割方式
    # archive_list = Article.objects.dates("create_date", 'month', order='DESC')
    # 结果类似于： [(2016, [11, 1]), (2015, [11])]
    archive_list = Article.objects.distinct_dates_api()
    # 获取友链
    Links_list = Link.objects.filter(is_publish=True)

    # 获取标签云
    # Tag_list = Tag.objects.all()
    Tag_list = Tag.objects.annotate(num_posts=Count('article'))

    # 点击排行
    clickCount_list = Article.objects.filter(is_publish=True).order_by("-click_count")[:6]

    # 站长推荐
    publish_list = Article.objects.filter(is_publish=True, is_recommend=True).order_by("-modify_date")[:6]

    SITE_NAME = settings.SITE_NAME
    SITE_KEY = settings.SITE_KEY
    SITE_DESC = settings.SITE_DESC
    classtagname = ["tagc1", "tagc2", "tagc3", "tagc4", "tagc5"]

    return {
        "SITE_NAME": SITE_NAME,
        "SITE_KEY": SITE_KEY,
        "SITE_DESC": settings.SITE_DESC,
        "category_list": category_list,
        "archive_list": archive_list,
        "Links_list": Links_list,
        "Tag_list": Tag_list,
        "clickCount_list": clickCount_list,
        "publish_list": publish_list,
        "classtagname": classtagname,
    }


# 分页代码
def getPage(request, article_list, pageArticleNum=5):
    page_paginator = Paginator(article_list, pageArticleNum)
    try:
        page = int(request.GET.get("page", 1))
        article_list = page_paginator.page(page)
    # except Exception as e:
    except (EmptyPage, InvalidPage, PageNotAnInteger) as e:
        logger.error(e)
        # 出错默认跳转至第一页
        article_list = page_paginator.page(1)
    return article_list


# 首页视图
def index(request):
    """
    """
    try:
        # 分类信息获取(导航数据)(已设置全局变量)
        # category_list = Category.objects.all()[:5]
        # 获取文章归档，使用的是自定义的方法 (已设置全局变量)
        # archive_list = Article.objects.distinct_date()
        # 最新文章,默认按照修改时间排序
        article_list = Article.objects.filter(is_publish=True).order_by("-create_date")
        article_list = getPage(request, article_list, 5)
    except Exception as e:
        logger.error(e)
    return render(request, 'blog/article_list.html', locals())


# 文章详情页
def articleDetail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 浏览一次 ，点击次数加1
    article.click_count += 1
    article.save()
    return render(request, 'blog/detail.html', locals())


# 文章归档代码
def pigeonhole(request):
    try:
        # 首先获取用户提交的数据
        year = request.GET.get("year", None)
        month = request.GET.get("month", None)
        article_list = get_list_or_404(Article, create_date__icontains=year + "-" + month, is_publish=True)
        # article_list = Article.objects.filter(create_date__icontains=year + "-" + month).filter(is_publish=True)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    mes_title = "%s年%s月文章" % (request.GET['year'], request.GET['month'])
    return render(request, 'blog/article_list.html', locals())


# 标签云视图
def tag(request, tag_name):
    try:
        # 首先获取用户提交的数据
        # article_list = get_list_or_404(Article, tags__name=tag_name, is_publish=True)
        article_list = Article.objects.filter(tags__name=tag).filter(is_publish=True)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    mes_title = "%s 标签下的文章" % (tag_name, )
    return render(request, 'blog/article_list.html', locals())


# 分类视图
def category(request, category_name):
    try:
        # article_list = get_list_or_404(Article, category__name=category_name, is_publish=True)
        article_list = Article.objects.filter(tags__name=tag, is_publish=True)
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    mes_title = "%s 分类下的文章" % (category_name, )
    return render(request, 'blog/article_list.html', locals())


# 申请友情链接
def applyLink(request):
    if request.method == "POST" and request.POST:
        # 如果是POST,接收用户输入
        link_form = LinkForm(request.POST)
        # 表单验证
        if link_form.is_valid():
            link_form.save()
            return HttpResponse("申请成功,请稍后我将尽快审核")
    else:
        link_form = LinkForm()
    locs = {
        "link_form": link_form,
    }
    return render(request, 'blog/LinkApply.html', locs)


# 搜索
def search(request):
    # 获取用户输入
    try:
        search_field = request.GET.get('search').strip()
    except Exception as e:
        # 不是POST请求过来的 另外处理
        return render(request, 'blog/search.html', locals())
    else:
        # 根据用户输入做个简单的标题模糊匹配
        article_list = Article.objects.filter(title__icontains=search_field, is_publish=True)
        article_list = getPage(request, article_list)
        mes_title = "%s 的搜索结果" % (search_field, )
        return render(request, 'blog/article_list.html', locals())


# 博客框架的demo
def demo(request):
    return render(request, 'blog/index2.html', locals())
