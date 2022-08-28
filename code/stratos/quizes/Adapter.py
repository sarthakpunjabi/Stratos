class IGetQuestionsJSON(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def RenderJSON():
        """Abstract interface"""
#Adaptee
class GetQuestionsJSON(ListView, IGetQuestionsJSON):
    model = Quiz
    template_name = 'quizes/main.html'

    def RenderJSON(request):    
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

class IGetQuestionsHTML(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def RenderHTML():
        """Abstract interface"""
#Target
class GetQuestionsHTML(ListView, IGetQuestionsHTML):
    def RenderHTML(request):
         return render(request,"quizes/add_quiz.html",context={"choices":default_categories})
#Adapter
#Makes JSON's iterface compatible with HTML's interface
class JSONToHTML(GetQuestionsJSON):
    def __init__(self):
        self.GetQuestionsJSON = GetQuestionsJSON()
    
    def RenderHTML(self):
        self.GetQuestionsJSON.RenderJSON()

class QuizListView(ListView):
    def add_quiz(request):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            ITEM = JSONToHTML()
        else:
            JSONObj = GetQuestionsJSON()
            ITEM = GetQuestionsHTML(JSONObj)
        ITEM.RenderHTML()