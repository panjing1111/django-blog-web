from django.shortcuts import render,redirect
import markdown
# Create your views here.
from django.http import HttpResponse
# 导入数据模型ArticlePost
from .models import ArticlePost
from .form import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# 引入分页模块
from django.core.paginator import Paginator
# 引入 Q 对象
from django.db.models import Q
# 类视图继承自View类
from django.views.generic import View
# 类视图的装饰器要通过method_decorator添加
from django.utils.decorators import method_decorator



# 文章列表
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search))
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()
    # 每页显示 2 篇文章
    paginator = Paginator(article_list, 6)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # 需要传递给模板（templates）的对象
    context = {'articles': articles, 'order': order, 'search': search }
    return render(request,'article/list.html',context)

# 指定作者的文章列表
def user_article_list(request,id):
    user = User.objects.get(id=id)
    article_list = ArticlePost.objects.filter(author=user)
    # # 每页显示 2 篇文章
    # paginator = Paginator(article_list, 6)
    # # 获取 url 中的页码
    # page = request.GET.get('page')
    # # 将导航对象相应的页码内容返回给 articles
    # articles = paginator.get_page(page)
    # # 需要传递给模板（templates）的对象
    context = {'articles': article_list,}
    return render(request,'article/list.html',context)

# 文章详情
def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 浏览量 +1
    article.total_views += 1
    # 指定只保存阅读量，减少服务器压力
    article.save(update_fields=['total_views'])
    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    context = {'article': article,'toc': md.toc}
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

# 写博客
@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        # 将POST数据交给ArticlePostForm处理，创建了一个实例
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据
            new_article = article_post_form.save(commit=False)
            # 指定目前登录的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        else:
            # 返回错误提示
            return HttpResponse("表单内容有误，请重新填写。")
    elif request.method == 'GET':
        # 同上创建表单类实例,不过是空的
        article_post_form = ArticlePostForm()
        context = {"article_post_form":article_post_form}
        return render(request,'article/create.html',context)

# 将写博客的功能由函数视图改为类视图
class ArticleCreateView(View):
    # 给get与post方法都添加装饰器，在点击写博客的按钮和提交博客按钮时候都要检查
    # 用户是否登录，只有登录才能执行这两个操作
    # todo 需增加功能，登录后返回登录前的页面
    @method_decorator(login_required(login_url='/userprofile/login/'))
    def get(self,request):
        '''创建一个空表单，返回到浏览器中'''
        article_post_form = ArticlePostForm()
        context = {"article_post_form":article_post_form}
        return render(request,'article/create.html',context)

    @method_decorator(login_required(login_url='/userprofile/login/'))
    def post(self,request):
        '''获取提交的数据，将其保存，然后返回到首页'''
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect('article:article_list')


# 删除文章
@login_required(login_url='/userprofile/login/')
def article_delete(request,id):
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    if article.author == request.user:
        article.delete()
        # 完成删除后返回文章列表
        return redirect("article:article_list")
    else:
        return HttpResponse("没有权限删除文章")



# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 判断是否是文章的作者
    if article.author == request.user:
        # 判断用户是否为 POST 提交表单数据
        if request.method == "POST":
            # 将提交的数据赋值到表单实例中
            article_post_form = ArticlePostForm(data=request.POST)
            # 判断提交的数据是否满足模型的要求
            if article_post_form.is_valid():
                # 保存新写入的 title、body 数据并保存
                article.title = request.POST['title']
                article.body = request.POST['body']
                article.save()
                # 完成后返回到修改后的文章中。需传入文章的 id 值
                return redirect("article:article_detail", id=id)
                # 如果数据不合法，返回错误信息
            else:
                return HttpResponse("表单内容有误，请重新填写。")
                # 如果用户 GET 请求获取数据
        else:
            # 创建表单类实例
            article_post_form = ArticlePostForm()
            # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
            context = {'article': article, 'article_post_form': article_post_form}
            # 将响应返回到模板中
            return render(request, 'article/update.html', context)
    else:
        return HttpResponse("没有权限编辑文章")