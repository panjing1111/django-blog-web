from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
import random

# Create your models here.


class ArticlePost(models.Model):
    objects = models.Manager()
    '''文章的数据模型'''
    # 文章作者是外键类型。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    # 文章标题。字符串字段，用于保存较短的字符串，比如标题,最大为30个字符
    title = models.CharField(max_length=30)

    # 文章正文。保存大量文本使用
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时  自动  写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 浏览量
    total_views = models.PositiveIntegerField(default=random.randint(1,10))


    class Meta:
        '''
        内部类 class Meta 用于给 model 定义元数据(任何不是字段的东西)
        排序选项ordering、数据库表名db_table、单数和复数名称verbose_name和 verbose_name_plural。
        '''
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

        # def __str__(self):
        #     # return self.title 将文章标题返回
        #     return self.title
