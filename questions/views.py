#!/usr/bin/env python3

from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse

from questions.models import Answer, Question
from questions import forms


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


def new_question(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.NewQuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question_detail', kwargs={
                'pk': question.pk,
                }))
    else:
        form = forms.NewQuestionForm()
    return render(request, 'questions/new-question.html', {
        'form': form,
        })


def new_answer(request, pk):
    question = Question.load_question(pk)
    answer = Answer(question=question)
    if request.method == 'POST':
        form = forms.NewAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save()
            return redirect(reverse('question_detail', kwargs={
                'pk': question.pk,
                }))
        print('El formulario no es valido')
        print(form.errors)
    else:
        form = forms.NewAnswerForm(instance=answer)
    return render(request, 'questions/new-answer.html', {
        'question': question,
        'form': form,
        })


def edit_question(request, pk):
    question = Question.load_question(pk)
    if request.method == 'POST':
        form = forms.EditQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect(reverse('question_detail', kwargs={
                'pk': question.pk,
                }))
    else:
        form = forms.EditQuestionForm(instance=question)
    return render(request, 'questions/edit-question.html', {
        'question': question,
        'form': form,
        })


def edit_answer(request, pk):
    answer = Answer.load_answer(pk)
    question = answer.question
    if request.method == 'POST':
        form = forms.EditAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save()
            return redirect(reverse('question_detail', kwargs={
                'pk': question.pk,
                }))
    else:
        form = forms.EditAnswerForm(instance=answer)
    return render(request, 'questions/edit-answer.html', {
        'answer': answer,
        'question': question,
        'form': form,
        })
