# django自带的视图
from django.contrib.auth import views as auth_views
# 自定义的视图
from . import views
from django.urls import path
app_name = 'account'

urlpatterns = [
    # 客户端访问路径：127.0.0.1:8000/login
    # 对应模板：account/login.html
    # 在模板中使用的名称为：user_login    如：action="{% url 'account:user_login' %}"
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='user_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='user_logout'),
    path('register/', views.register, name='user_register')

]