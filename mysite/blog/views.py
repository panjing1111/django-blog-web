from django.shortcuts import render,get_object_or_404
from .models import BlogArticles



def blog_title(request):
    blogs = BlogArticles.objects.all()
    # render将数据渲染到模板
    return render(request,'blog/titles.html',{'blogs':blogs})


def blog_article(request, article_id):
    article = get_object_or_404(BlogArticles, id=article_id)
    publish = article.publish
    return render(request,'blog/content.html',{'article':article,'publish':publish})

def add_blog(request):
    '''发表博客'''
