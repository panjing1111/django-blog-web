
from django.db import models
from django.contrib.auth.models import User
# 引入信号接收器的装饰器
from django.dispatch import receiver
# 引入内置信号
from django.db.models.signals import post_save



# Create your models here.
# ，每次改动模型后都需要进行数据的迁移
class Profile(models.Model):
    '''扩展用户类'''
    objects = models.Manager()
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)

'''
如果从后台直接写入Profile的数据就会报错，因为Profile会随着user的创建而主动创建，
相当于创建了2次，违背了一对一的关系：OneToOneField

# 信号接收函数，每当新建 User 实例时自动调用
@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 信号接收函数，每当更新 User 实例时自动调用
def save_user_profile(sender,instance, **kwargs):
    instance.profile.save()
'''