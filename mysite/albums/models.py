from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class PersonalPhoto(models.Model):
    '''个人相册模型'''
    object = models.Manager()
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=False)
    # 图片上传到upload_images
    body = models.FileField(upload_to='images/upload_images/%Y%m%d/')
    upload_time = models.DateTimeField(default=timezone.now) # 照片上传时间

    class Meta:
        # BlogArticles实例对象的显示顺序为publish的倒序
        ordering = ('-upload_time',)

    def __str__(self):
        return self.title