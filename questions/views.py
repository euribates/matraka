from django.shortcuts import render
from django.db.models import Count

from questions.models import Question

# Create your views here.
def all_questions(request):
    questions = (
        Question.objects.all()
        .annotate(num_answers=Count('answers'))
        )
    return render(request, 'questions/all_questions.html', {
        'questions': questions,
        })



def question_detail(request, pk):
    question = Question.load_question(pk)
    return render(request, 'questions/question-detail.html', {
        'question': question,
        'answers': list(question.answers.all()),
        })
