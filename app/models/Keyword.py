from django.db import models


# {问题关键词} <=[问题]
class Keyword(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    @classmethod
    def to_json(cls):
        return {
            'keywords': [kw.name for kw in Keyword.objects.all()]
        }
