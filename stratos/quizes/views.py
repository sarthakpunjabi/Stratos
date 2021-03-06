from urllib import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Quiz
from django.views.generic import ListView
from django.http import JsonResponse,HttpResponse
from questions.models import Answer, Question
from results.models import Result
from django.shortcuts import redirect
from .memento import Memento,Originator,Caretaker
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import requests

# Create your views here.

default_categories = {}

temp_categories = ["General Knowledge",
"Books","Film","Music","Musicals & Theatres",
"Television","Video Games","Board Games",
"Science & Nature","Science Computers",
"Science Mathematics","Mythology","Sports",
"Geograpy","History","Politics",
"Art","Celebrities","Animals",
"Vehicles","Comics","Gadgets",
"Japanese","Cartoon & Animations"
]

for index,value in enumerate(temp_categories):
    default_categories[index+9]=value


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.html'
    


def add_quiz(request):
    request.log.info("Adding the quiz")
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        temp = request.POST
        parameters = {
            "amount":int(temp['amount']),
            "category":int(temp['choice']),
            "difficulty":temp['difficulty'],
            "type":temp['type']
        }
        data = requests.get("https://opentdb.com/api.php",params=parameters).json()["results"]
        
        return JsonResponse({
            'data':data,
        })
    else:    
        return render(request,"quizes/add_quiz.html",context={"choices":default_categories})

@login_required
def add_save(request):
    request.log.info("Saving the quiz")
    data = request.POST
    data_ = dict(data.lists())
    obj = Originator(data_)
    obj.adding_quiz()
    
    return JsonResponse({"Objective":"Achieved"})


@login_required
def remove_save(request):
    request.log.info("Removing the quiz")
    print("Entered the remove state")
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = request.POST
        obj2 = Caretaker()
        obj = Memento(data)
        obj.rem()
        
    return JsonResponse({"Objective":"Achieved and Removed "})


@login_required
def quiz_view(request,pk):
    request.log.info("Getting the quiz")
    quiz = Quiz.objects.get(pk=pk)
    return render(request,'quizes/quiz.html',{'obj':quiz})

@login_required
def quiz_data_view(request,pk):
    request.log.info("Storing the questions and answers")
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_question():
        answers = []
        for a in q.get_answer():
            answers.append(a.text)
        questions.append({str(q):answers})
    
    return JsonResponse({
        'data':questions,
        'time':quiz.time,
    })

@login_required
def save_quiz_view(request,pk):
    request.log.info("Saving the quiz result")
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        print(data_)

        for k in data_.keys():
            question = Question.objects.get(text=k)
            print(question)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)
        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            print('a_select',a_selected)
            if a_selected != "":
                question_answer = Answer.objects.filter(question=q)
                
                for a in question_answer:
                    if a_selected == a.text:
                        
                        if a.correct:
                            score +=1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                
                results.append({str(q):{'correct_answer':correct_answer,'answered':a_selected}})
            else:
                results.append({str(q):'not answered'})

        score_ = score * multiplier 
        Result.objects.create(quiz=quiz,user=user,score=score_)
        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed':True,'score':score_,'results':results})
        else:
            return JsonResponse({'passed':False,'score':score_,'results':results})