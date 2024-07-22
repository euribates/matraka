#!/usr/bin/env python3

from django.contrib import admin
from django.urls import path, include

import main.views
import questions.views


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', main.views.index),
    tie('login/', main.views.user_login),
    tie('logout/', main.views.user_logout),
    tie('ask/', questions.views.ask_question),
    tie('ask/<int:pk>/', questions.views.ask_question),
    tie('ask/<slug:tag>/', questions.views.ask_by_tag),
    tie('chk/<int:pk>/', questions.views.chk_answer),
    tie('search/', questions.views.search),
    path('questions/', include('questions.urls')),
    path('api/', include('api.urls')),
    path("admin/", admin.site.urls),
    ]
