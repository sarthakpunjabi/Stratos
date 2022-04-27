#Subsystem 1    

from questions.models import Question,Answer
from .models import Quiz

class Score:       
   def GetScore(self,question_answer,a_selected):   
      for a in question_answer:
                    if a_selected == a.text:
                        
                        if a.correct:
                            score +=1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text   
  
#Subsystem 2  
class Questions:  
   def GetQuestions(self,request,data):   
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        print(data_)

        for k in data_.keys():
            question = Question.objects.get(text=k)
            print(question)
            questions.append(question)
            return questions
  
#Subsystem 3  
class Answers:   
   def GetAnswers(self,request,questions):   
      for q in questions:
            a_selected = request.POST.get(q.text)
            print('a_select',a_selected)
            if a_selected != "":
                question_answer = Answer.objects.filter(question=q)
                for a in question_answer:
                    if a_selected == a.text:
                        print("DOne")
                        return q
               
  
class Operator:
    def __init__(self):   
        self.Creating = Score()  
        self.Generating = Questions()   
        self.delivering = Answers()  
    
    def completeOrder(self):  
        self.Creating.GetScore()  
        self.Generating.GetQuestions()  
        self.delivering.GetAnswers()
        print("Quiz Created successfully")  
