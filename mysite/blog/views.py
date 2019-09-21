from django.shortcuts import render
from .models import BlogArticles



def blog_title(request):
    blogs = BlogArticles.objects.all()
    # render将数据渲染到模板
    return render(request,'blog/titles.html',{'blogs':blogs})

