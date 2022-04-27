'''
        Results Model
    '''
from django.conf import settings
from django.db import models
from quizes.models import Quiz

User = settings.AUTH_USER_MODEL

# Create your models here.
class Result(models.Model):
    '''
        Results Model
    '''
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return self.pk
