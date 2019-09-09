from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm
# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm
# 类视图继承自View类
from django.views.generic import View
# 类视图的装饰器要通过method_decorator添加
from django.utils.decorators import method_decorator
# from allauth.account.views import LoginView

# Create your views here.

# 用户登录
class UserLoginView(View):
    def get(self,request):
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)

    def post(self,request):
        user_login_form = UserLoginForm(request.POST)
        if user_login_form.is_valid():
            # 清洗数据
            data = user_login_form.cleaned_data
            # 检验账号是否正确
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse("账号或密码输入有误。请重新输入~")
        else:
            return HttpResponse("账号或密码输入不合法~")

# class UserLoginView(LoginView):
#     pass


# 用户退出
def user_logout(request):
    logout(request)
    return redirect("article:article_list")


# 用户注册
class UserRegisterView(View):
    def get(self,request):
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)

    def post(self,request):
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 密码
            new_user.set_password(user_register_form.cleaned_data.get('password'))
            new_user.save()
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

# # 用户删除
# @login_required(login_url='/userprofile/login/')
# def user_delete(request, id):
#     '''加装饰器后 执行本函数会检测用户是否登录，如果没有登录，就重定向到登录界面'''
#     user = User.objects.get(id=id)
#     if request.user == user:
#         # 退出登录后删除用户
#         logout(request)
#         user.delete()
#         return redirect("article:article_list")
#     else:
#         return HttpResponse("你没有删除操作的权限。")


# 编辑用户信息 (name='dispatch'代表给这个类的所有方法都添加装饰器)
@method_decorator(login_required(login_url='/userprofile/login/'), name='dispatch')
class UserEditView(View):
    def get_user(self,id):
        '''初始化获取用户信息'''
        user = User.objects.get(id=id)
        # profile通过id获取到用户对象的所有扩展属性
        if Profile.objects.filter(user_id=id).exists():
            profile = Profile.objects.get(user_id=id)
        else:
            profile = Profile.objects.create(user=user)
        return user,profile

    def get(self,request,id):
        user,profile = self.get_user(id)
        profile_form = ProfileForm()
        context = {'profile_form': profile_form, 'profile': profile, 'user': user}
        return render(request, 'userprofile/edit.html', context)

    def post(self,request,id):
        user, profile = self.get_user(id)
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")