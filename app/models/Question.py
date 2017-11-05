from django.db import models
from .User import User
from .Keyword import Keyword


# [问题] ->[用户] & =>{问题关键词} & <=[答案]
class Question(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, help_text='题主')
    content = models.TextField(help_text='问题内容')
    keywords = models.ManyToManyField('Keyword', help_text='问题关键字')

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[%s] %s' % (self.user and self.user.username or 'Anonymous', self.content[:10])

    @classmethod
    def find_alike(cls,ques):
        keywords=ques['keywords']
        key_list=keywords.split(' ')
        for word in key_list:
            print ("\n key is " + word + "\n")
        try:
            q = Question.objects.filter(keywords__name = keywords)
        except Question.DoesNotExist:
            return False
        if q:
            if q[0]:
                return q[0].id
        return False

    @classmethod
    def update_questionlist(cls, dist):
        u = User.objects.get(uid = dist['uid'])
        p,created = Keyword.objects.get_or_create(name = dist['keywords'])
        q,created = Question.objects.get_or_create(user = u,content = dist['question'])
        q.keywords.add(p)
        return q
