"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import main.views
import questions.views


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', main.views.index),
    tie('ask/', questions.views.ask),
    tie('ask/<int:pk>/', questions.views.ask),
    tie('questions/', questions.views.all_questions),
    tie('questions/new/', questions.views.new_question),
    tie('questions/<int:pk>/', questions.views.question_detail),
    tie('questions/<int:pk>/add/', questions.views.new_answer),
    tie('questions/<int:pk>/edit/', questions.views.edit_question),
    tie('answer/<int:pk>/edit/', questions.views.edit_answer),
    tie('search/', questions.views.search),
    path("admin/", admin.site.urls),
    ]
