#!/usr/bin/env python3

import random

from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy

from questions import models
from questions import forms


def all_questions(request):
    questions = (
        models.Question.objects.all()
        .annotate(num_answers=Count('answers'))
        )
    return render(request, 'questions/all_questions.html', {
        'questions': questions,
        })


def ask(request, pk=0):
    if pk:
        question = models.Question.load_question(pk)
    else:
        question = random.choice(models.Question.objects.all())
    answers = dict(zip('ABCD', question.get_random_answers()))
    form = forms.AskForm()
    return render(request, 'questions/ask.html', {
        'titulo': f'Pregunta {question.pk}: {question.text}',
        'question': question,
        'answers': answers,
        'form': form,
        })


def chk_answer(request, pk):
    answer = models.Answer.load_answer(pk)
    return render(request, 'questions/chk.html', {
        'titulo': 'Respuesta válida' if answer.is_correct else 'No es correcta',
        'answers': answer,
        })


def question_detail(request, pk):
    question = models.Question.load_question(pk)
    form = forms.NewAnswerForm(question)
    return render(request, 'questions/question-detail.html', {
        'titulo': f'Detalles pregunta {pk}',
        'question': question,
        'answers': list(question.answers.all()),
        'form': form,
        })


def new_question(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.NewQuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(reverse_lazy('question_detail', kwargs={
                'pk': question.pk,
                }))
    else:
        form = forms.NewQuestionForm()
    return render(request, 'questions/new-question.html', {
        'form': form,
        })


def new_answer(request, pk):
    question = models.Question.load_question(pk)
    if request.method == 'POST':
        form = forms.NewAnswerForm(question, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('question_detail', kwargs={
                'pk': question.pk,
                }))
        print('El formulario no es valido')
        print(form.errors)
    else:
        form = forms.NewAnswerForm(question)
    return render(request, 'questions/new-answer.html', {
        'question': question,
        'form': form,
        })


def edit_question(request, pk):
    question = models.Question.load_question(pk)
    if request.method == 'POST':
        form = forms.EditQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect(reverse_lazy('question_detail', kwargs={
                'pk': question.pk,
                }))
    else:
        form = forms.EditQuestionForm(instance=question)
    return render(request, 'questions/edit-question.html', {
        'question': question,
        'form': form,
        })


def edit_answer(request, pk):
    answer = models.Answer.load_answer(pk)
    question = answer.question
    if request.method == 'POST':
        form = forms.EditAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save()
            return redirect(reverse_lazy('question_detail', kwargs={
                'pk': question.pk,
                }))
    else:
        form = forms.EditAnswerForm(instance=answer)
    return render(request, 'questions/edit-answer.html', {
        'answer': answer,
        'question': question,
        'form': form,
        })


def search(request, *args, **kwargs):
    results = []
    if request.method == 'POST':
        form = forms.SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            questions = models.Question.objects.filter(text__icontains=query)
            for question in questions:
                results.append({
                    'pk': question.pk,
                    'url': question.get_absolute_url(),
                    'text': question.text,
                    'tag': 'Q',
                    'question': question,
                    })
            answers = models.Answer.objects.filter(text__icontains=query)
            for answer in answers:
                results.append({
                    'pk': answer.question.pk,
                    'url': answer.question.get_absolute_url(),
                    'text': answer.text,
                    'tag': 'A',
                    'answer': answer,
                    })
    else:
        query = request.GET.get('query', '')
        form = forms.SearchForm(initial={'query': query})
    return render(request, 'questions/search.html', {
        'titulo': 'Buscador',
        'form': form,
        'results': results,
        'num_results': len(results),
        })
