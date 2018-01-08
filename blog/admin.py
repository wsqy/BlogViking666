from django.contrib import admin
from blog.models import Tag, Category, Article, Link


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 定义前端显示的
    list_display = ('id', 'name', 'SubClass', 'Weights',)
    # 定义前端可编辑的
    list_editable = ('name', 'SubClass', 'Weights',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'Weights',)
    list_editable = ('name', 'Weights',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_publish', 'is_recommend', 'is_original')
    list_display_links = ('id', 'title', )
    search_fields = ('title', )
    fieldsets = (
        (None, {
            'fields': ('title', 'url', 'desc', ('is_publish', 'is_recommend', 'click_count',),),
        }),
        ('时间', {
            'classes': ('collapse',),
            'fields': ('create_date', 'modify_date'),
        }),
        ('分类信息', {
            # 'classes': ('collapse',),
            'fields': ('tags', 'category',)
        }),
        ('文章信息', {
            # 'classes': ('collapse',),
            'fields': ('Content',)
        }),
        ('原创', {
            # 'classes': ('collapse',),
            'fields': ('is_original', 'url_old', 'website')
        }),
    )


# 注册action 批量通过申请
def confirm_publish(modeladmin, request, queryset):
    queryset.update(is_publish=True)
confirm_publish.short_description = "通过选中的申请"


@admin.register(Link)
class originateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url', 'Weights', 'is_publish', )
    list_editable = ('name', 'Weights', 'is_publish', )
    actions = (confirm_publish, )

# Register your models here.
# admin.site.register(website)
# admin.site.register(Tag)
# admin.site.register(Category)
# admin.site.register(Article)
# admin.site.register(link)
