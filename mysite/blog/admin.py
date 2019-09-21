from django.contrib import admin
from .models import BlogArticles



class BlogArticlesAdmin(admin.ModelAdmin):
    list_display = 'title','author','publish','body'
    list_filter = 'publish','author'
    search_fields = 'title','body'
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['publish','author']




# 给admin注册BlogArticles模型，admin就可以自动添加创建文章的功能
admin.site.register(BlogArticles,BlogArticlesAdmin)
