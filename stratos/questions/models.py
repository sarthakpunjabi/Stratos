from django.db import models
from quizes.models import Quiz

<<<<<<< HEAD
# Create your models here.
=======
# the child classes that inherits the main parent class
>>>>>>> factory-pattern

class Question(models.Model):
    text = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

<<<<<<< HEAD
    def __str__(self):
        return str(self.text)

=======
    @staticmethod
    def __str__(self):
        return str(self.text)

    @staticmethod
>>>>>>> factory-pattern
    def get_answer(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD

=======
    
    @staticmethod
>>>>>>> factory-pattern
    def __str__(self):
        return f"question: {self.question.text}, answer:{self.text} correct:{self.correct}"