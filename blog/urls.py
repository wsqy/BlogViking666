# coding:utf-8
from blog.views import index, pigeonhole, tag, articleDetail, category, applyLink, search, demo
from django.conf.urls import include, url

app_name = 'blog'

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^index$', index, name='index'),
    url(r'^pigeonhole$', pigeonhole, name='pigeonhole'),
    url(r'^tag/(?P<tag_name>.+)$', tag, name='tag'),
    url(r'^article/(?P<article_id>\d+)$', articleDetail, name='article'),
    url(r'^category/(?P<category_name>.+)$', category, name='category'),
    url(r'^applyLink$', applyLink, name='applyLink'),
    url(r'^search$', search, name='search'),


    # 测试样例
    url(r'^demo$', demo, name='demo'),

]
