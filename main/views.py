#!/usr/bin/env python3

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from main.forms import LoginForm
from questions.models import Question


def index(request):
    num_questions = Question.objects.all().count()
    return render(request, 'index.html', {
        'num_questions': num_questions,
        })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect(reverse_lazy('index'))
    else:
        form = LoginForm()
    return render(request, "login.html", {
        'titulo': 'Identificación de usuario',
        'form': form,
        })


def user_logout(request):
    logout(request)
    return redirect(reverse_lazy('index'))
