from django.contrib import admin
from .models import BlogArticles


class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = 'title','author','publish'


# 给admin注册BlogArticles模型，admin就可以自动添加创建文章的功能
admin.site.register(BlogArticles,BlogArticlesAdmin)
