from django.db import models
from .Tag import Tag


# [用户] =>{用户标签} & <=[问题]|[答案]
class User(models.Model):
    uid = models.CharField(null=True, blank=True, max_length=128, help_text='所依赖的聊天工具平台上用户唯一标识')
    username = models.CharField(unique=True, max_length=64, help_text='注册/登录名')
    realname = models.CharField(null=True, blank=True, max_length=64, help_text='实名')
    _GENDER = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    gender = models.PositiveSmallIntegerField(blank=True, choices=_GENDER, default=0)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=11)
    tags = models.ManyToManyField(Tag)

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[%d]: %s' %(self.id, self.username)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'tags': [t.name for t in self.tags.all()]
        }