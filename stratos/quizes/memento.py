import html
from .models import Quiz
from questions.models import Answer, Question


class Memento:
    def __init__(self):
        self.state_history = []




class Add(Memento):
    def __init__(self,data_):
        self.data_ = data_

    def adding_quiz(self):
        try:
            access = Quiz.objects.get(name=f"{self.data_.get('meta[nameofquiz]')[0]}")
            return access
        
        except:
            # super.state_history.add("")
            Q,create = Quiz.objects.get_or_create(
                name=f"{self.data_.get('meta[nameofquiz]')[0]}",
                topic = f"{self.data_.get('meta[topic]')[0]}",
                number_of_questions = f"{self.data_.get('meta[numberofquestion]')[0]}",
                time = f"{self.data_.get('meta[time]')[0]}",
                required_score_to_pass = f"{self.data_.get('meta[reqscoretopass]')[0]}",
                difficulty = f"{self.data_.get('meta[difficulty]')[0]}",
            )
            if create:
                for i in range(int(Q.number_of_questions)):
                    print(html.unescape(f"{self.data_.get(f'data[{i}][question]')[0]}"))
                    que = Question.objects.get_or_create(
                        text = html.unescape(f"{self.data_.get(f'data[{i}][question]')[0]}"),
                        quiz_id = Q.id
                    )
                    print(html.unescape(f"{self.data_.get(f'data[{i}][correct_answer]')[0]}"))
                    ans = Answer.objects.get_or_create(
                        text = html.unescape(f"{self.data_.get(f'data[{i}][correct_answer]')[0]}"),
                        correct = True,
                        question_id = que[0].id
                    )
                    ans1 = Answer.objects.get_or_create(text = html.unescape(f"{self.data_.get(f'data[{i}][incorrect_answers][]')[0]}"),correct=False,question_id=f"{que[0].id}"),
                    ans2 = Answer.objects.get_or_create(text = html.unescape(f"{self.data_.get(f'data[{i}][incorrect_answers][]')[1]}"),correct=False,question_id=f"{que[0].id}"),
                    ans3 = Answer.objects.get_or_create(text = html.unescape(f"{self.data_.get(f'data[{i}][incorrect_answers][]')[2]}"),correct=False,question_id=f"{que[0].id}"),


class Remove:
    def __init__(self):
        pass