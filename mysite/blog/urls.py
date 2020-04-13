from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('',views.blog_title,name='blog_title'),
    path('<int:article_id>',views.blog_article,name='blog_article'),
    # name的作用：在模板中url使用name调用函数，如使用blog_article代表调用views.blog_article函数
]