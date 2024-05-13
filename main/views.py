#!/usr/bin/env python3

from django.shortcuts import render

from questions.models import Question


def index(request):
    num_questions = Question.objects.all().count()
    return render(request, 'index.html', {
        'num_questions': num_questions,
        })
