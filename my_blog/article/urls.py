from django.urls import path
from . import views
# 正在部署的应用的名称 django2.0后必须有app_name
app_name = 'article'

# 文章有文章列表页与文章详情页 需要添加到urlpatterns中
urlpatterns = [
    # path函数将url映射到视图
    path('article-list/', views.article_list, name='article_list'),
    path('user-article-list/<int:id>/', views.user_article_list, name='user_article_list'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article-create/', views.ArticleCreateView.as_view(), name='article_create'),
    # path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    path('article-update/<int:id>/', views.article_update, name='article_update'),
]
