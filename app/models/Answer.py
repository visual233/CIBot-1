from django.db import models
from .User import User
from .Question import Question


# [答案] ->[用户]|[问题]
class Answer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, help_text='答主|为空时意为搜索引擎')
    question = models.ForeignKey(Question, help_text='对应的问题')
    content = models.TextField(help_text='答案内容')
    grade = models.PositiveSmallIntegerField(blank=True, default=3, help_text='评分1-5')
    like = models.PositiveIntegerField(blank=True, default=0, help_text='赞同数')
    dislike = models.PositiveIntegerField(blank=True, default=0, help_text='反对数')

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[%s] %s' % (self.user.username, self.content[:10])

    @classmethod
    def update_answerlist(cls, dist):
        try:
            u = User.objects.get(uid = dist['uid'])
            q = Question.objects.get(qid = dist['qid'])
            a, created = Answer.objects.get_or_create(user=u, content=dist['answer'], question=q)
        except:
            print("poinson")

    @classmethod
    def qid_get_ans_con(cls,qid):
        ans = Answer.objects.get(qid = qid).content
        return ans
