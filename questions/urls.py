#!/usr/bin/env python3

from django.urls import path


from . import views


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', views.all_questions),
    tie('new/', views.new_question),
    tie('<int:pk>/', views.question_detail),
    tie('<int:pk>/edit/', views.edit_question),
    tie('answer/<int:pk>/add/', views.new_answer),
    tie('answer/<int:pk>/edit/', views.edit_answer),
    ]
