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
from django.urls import path, include

import main.views
import questions.views


def tie(ruta, vista, name=None):
    return path(ruta, vista, name=name or vista.__name__)


urlpatterns = [
    tie('', main.views.index),
    tie('ask/', questions.views.ask_question),
    tie('ask/<int:pk>/', questions.views.ask_question),
    tie('ask/<slug:tag>/', questions.views.ask_by_tag),
    tie('chk/<int:pk>/', questions.views.chk_answer),
    tie('search/', questions.views.search),
    path('questions/', include('questions.urls')),
    path('api/', include('api.urls')),
    path("admin/", admin.site.urls),
    ]
