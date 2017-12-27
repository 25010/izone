# 创建了新的tags标签文件后必须重启服务器

from django import template
from ..models import Article, Category, Tag, Timeline, Carousel, Keyword
from django.db.models.aggregates import Count
from django.utils.html import mark_safe

register = template.Library()


# 文章相关标签函数
@register.simple_tag
def get_article_list(sort=None,num=None):
    '''获取所有文章'''
    if sort == '-views':
        if num:
            return Article.objects.order_by('-views', '-update_date')[:num]
        return Article.objects.order_by('-views', '-update_date')
    if num:
        return Article.objects.all()[:num]
    return Article.objects.all()



@register.simple_tag
def keywords_to_str(art):
    '''将文章关键词变成字符串'''
    keys = art.keywords.all()
    return ','.join([key.name for key in keys])

@register.simple_tag
def get_tag_list():
    '''返回标签列表'''
    return Tag.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

@register.simple_tag
def get_category_list():
    '''返回分类列表'''
    return Category.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)

@register.inclusion_tag('blog/tags/article-list.html')
def load_article_summary(articles):
    '''返回文章列表模板'''
    return {'articles':articles}

@register.inclusion_tag('blog/tags/pagecut.html',takes_context=True)
def load_pages(context):
    '''分页标签模板，不需要传递参数，直接继承参数'''
    return context

# 其他函数
@register.simple_tag
def get_carousel_list():
    '''获取轮播图片列表'''
    return Carousel.objects.all()

@register.simple_tag
def get_star(num):
    '''得到一排星星'''
    tag_i = '<i class="fa fa-star"></i>'
    return mark_safe(tag_i * num)


@register.simple_tag
def get_star_title(num):
    '''得到星星个数的说明'''
    the_dict = {
        1: '【1颗星】：微更新，涉及轻微调整或者后期规划了内容',
        2: '【2颗星】：小更新，小幅度调整，一般不会迁移表格',
        3: '【3颗星】：中等更新，一般会增加或减少模块，有表格的迁移',
        4: '【4颗星】：大更新，涉及到应用的增减',
        5: '【5颗星】：最大程度更新，一般涉及多个应用和表格的变动',
    }
    return the_dict[num]