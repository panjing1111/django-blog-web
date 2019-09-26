from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# 文章模型
class BlogArticles(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=100)
    # 作者字段是一个外键，多对一
    # related_name 代表可以用过User的blog_posts反向查询到BlogArticles
    author = models.ForeignKey(User, on_delete=False, related_name='blog_posts')
    body = models.TextField()
    # 出版时间
    publish = models.DateTimeField(default=timezone.now)

    class Meta:
        # BlogArticles实例对象的显示顺序为publish的倒序
        ordering = ('-publish',)

    def __str__(self):
        return self.title
