#!/usr/bin/env python3

import random

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from questions import forms
from questions import links
from questions import models
from tags.models import Tag


def all_questions(request):
    questions = (
        models.Question.objects.all()
        .annotate(num_answers=Count('answers'))
        .order_by('-created_at')
        )
    paginator = Paginator(questions, 25)
    page_number = int(request.GET.get("page", '1'))
    return render(request, 'questions/all_questions.html', {
        'num_questions': questions.count(),
        'page': paginator.get_page(page_number),
        })


def ask_question(request, pk=0):
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


def ask_by_tag(request, tag):
    tag = Tag.load_tag(tag)
    questions = list(tag.questions.all())
    question = random.choice(questions)
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
    question = answer.question
    return render(request, 'questions/chk.html', {
        'titulo': 'Respuesta válida' if answer.is_correct else 'No es correcta',
        'answer': answer,
        'question': question,
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


@login_required
def new_question(request, *args, **kwargs):
    if request.method == 'POST':
        form = forms.NewQuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect(links.a_question_detail(question.pk))
    else:
        form = forms.NewQuestionForm()
    return render(request, 'questions/new-question.html', {
        'form': form,
        })


@login_required
def new_answer(request, pk):
    question = models.Question.load_question(pk)
    if request.method == 'POST':
        form = forms.NewAnswerForm(question, request.POST)
        if form.is_valid():
            form.save()
            return redirect(links.a_question_detail(question.pk))
        print('El formulario no es valido')
        print(form.errors)
    else:
        form = forms.NewAnswerForm(question)
    return render(request, 'questions/new-answer.html', {
        'question': question,
        'form': form,
        })


@login_required
def edit_question(request, pk):
    question = models.Question.load_question(pk)
    if request.method == 'POST':
        form = forms.EditQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect(links.a_question_detail(question.pk))
    else:
        form = forms.EditQuestionForm(instance=question)
    return render(request, 'questions/edit-question.html', {
        'question': question,
        'form': form,
        })


@login_required
def edit_answer(request, pk):
    answer = models.Answer.load_answer(pk)
    question = answer.question
    if request.method == 'POST':
        form = forms.EditAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save()
            return redirect(links.a_question_detail(question.pk))
    else:
        form = forms.EditAnswerForm(instance=answer)
    return render(request, 'questions/edit-answer.html', {
        'answer': answer,
        'question': question,
        'form': form,
        })


@csrf_exempt
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
