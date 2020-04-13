from django.db import models
from django.contrib.auth.models import User
# Create your models here.





# 创建用户模型 扩展django自带的User模型，如手机号
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    phone = models.CharField(max_length=20,null=True,unique=True)

    def __str__(self):
        return 'user {}'.format(self.user.name)