# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
# 引入 Profile 模型
from .models import Profile



# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    # forms.ModelForm，这个父类适合于需要直接与数据库交互的功能,如更新数据库
    # 需要手动配置每个字段，它适用于不与数据库进行直接交互的功能。
    username = forms.CharField()
    password = forms.CharField()


# 注册用户表单(注册用户的表单只有最基本的账号密码手机号，因此继承User模型就可)
class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")


# 用户编辑的表单(用户编辑的表单有其他用户属性，因此需继承扩展User后的模型：Profile)
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
