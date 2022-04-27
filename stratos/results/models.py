from django.db import models
from quizes.models import Quiz
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Result(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return self.pk