from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class TreeNode(models.Model):
    TYPE_CHOICES = (
        ('branch', '分支'),
        ('alarm', '报警'),
        ('screen', '聚合图形')
    )

    SPACE_CHOICES = (
        ('user', '用户'),
        ('organization', '组织'),
    )

    path = models.CharField(max_length=1024, unique=True, verbose_name='路径')
    text = models.CharField(max_length=254, verbose_name='文本')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='branch', verbose_name='类型')
    space = models.CharField(max_length=50, choices=SPACE_CHOICES, verbose_name='空间')
    owners = models.ManyToManyField(User, related_name='owners', blank=True, verbose_name='负责人')
    viewers = models.ManyToManyField(User, related_name='viewers', blank=True, verbose_name='观众')
    description = models.CharField(max_length=1024, null=True, blank=True, verbose_name='描述')
    settings = JSONField(default=dict, blank=True, verbose_name='设置')

    class Meta:
        verbose_name = 'TreeNode'

    def __str__(self):
        return str(self.path)


class History(models.Model):
    action = models.CharField(max_length=512, verbose_name='动作')
    data = JSONField(default=dict, blank=True, verbose_name='数据')
    action_user = models.CharField(max_length=512, verbose_name='用户')
    action_time = models.DateTimeField(auto_now_add=True, verbose_name='时间')

    class Meta:
        verbose_name = 'History'

    def __str__(self):
        return '%s %s' % (self.action_user, self.action)
