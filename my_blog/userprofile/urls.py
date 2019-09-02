from django.urls import path
from . import views
# 正在部署的应用的名称 django2.0后必须有app_name
app_name = 'userprofile'

# 文章有文章列表页与文章详情页 需要添加到urlpatterns中
urlpatterns = [
    # path函数将url映射到视图
    path('login/', views.user_login, name='login'),
    # path函数将url映射到视图
    path('logout/', views.user_logout, name='logout'),
    # 用户注册
    path('register/', views.user_register, name='register'),
#    用户删除
    path('delete/<int:id>/', views.user_delete, name='delete'),
# 用户信息
    path('edit/<int:id>/', views.profile_edit, name='edit'),

]