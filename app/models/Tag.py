from django.db import models


# {用户标签} <=[用户]
class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    @classmethod
    def to_json(cls):
        return {
            'tags': [t.name for t in Tag.objects.all()]
        }
